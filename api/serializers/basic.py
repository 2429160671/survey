from rest_framework import serializers
from django.template import loader
from web import models
from django.urls import reverse


# 序列化器，从此处获取数据，需要对数据进行加工则在此处进行
class SurveySerializer(serializers.ModelSerializer):

    grade = serializers.CharField(source="grade.name")
    valid_count = serializers.SerializerMethodField()     # 有效数量
    handle_link = serializers.SerializerMethodField()     # 调查链接
    handle = serializers.SerializerMethodField()          # 操作
    date = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = models.Survey
        fields = (
            "grade",
            "name",
            "valid_count",
            "times",
            "date",
            "handle_link",
            "handle"
        )

    # 方法加工数据，然后返回
    def get_valid_count(self, instance):
        # 有效填写人次
        return models.SurveyCode.objects.filter(survey=instance, is_used=True).count()

    def get_handle_link(self, instance):
        # 填写链接
        request = self.context.get("request")
        # 拼接填写链接，使用reverse反射来找到对应的链接，之后只需要修改urls.py
        link = "{}://{}{}".format(
            request.scheme,
            request.get_host(),
            reverse('survey_detail', args={instance.pk})
        )
        return "<a href='{}'>{}</a>".format(link, link)

    def get_handle(self, instance):
        return loader.render_to_string(
            "web/components/handle.html",
            context={
                "report_link": "",
                "download_link": f"/{instance.pk}/download/"
            }
        )


class SurveyChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SurveyChoice
        fields = "__all__"


class SurveyQuestionSerializer(serializers.ModelSerializer):
    # 添加的选项字段，反向查询
    # choices = serializers.SerializerMethodField()
    # 这种方法也可以，更方便
    # choices = SurveyChoiceSerializer(many=True, source="surveychoice_set.all")
    # 如果在models之中给SurveyChoice.questions加上了related_name，则可以这样进行反向查询,source都不用加了
    # 注意是relate_name和自定义的字段名相同，就不用加source
    choices = SurveyChoiceSerializer(many=True)
    value = serializers.CharField(default="", min_length=15, error_messages={
        'invalid': "类型无效",
        'blank': "输入不能为空",
        'min_length': "最少{max_length}个字",
    })
    error = serializers.CharField(default="", required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = models.SurveyQuestion
        fields = (
            "id",
            "survey_type",
            "title",
            "choices",
            "value",
            "error"
        )

    def get_choices(self, instance):
        # return models.SurveyChoice.objects.filter(question=instance.pk).values()
        # 取当前survey的所有choice
        return list(instance.surveychoice_set.values())


class SurveyTemplateSerializer(serializers.ModelSerializer):

    # 一对多关系，指定子序列化器
    questions = SurveyQuestionSerializer(many=True)

    class Meta:
        model = models.SurveyTemplate
        fields = (
            "id",
            "name",
            "questions"
        )


class SurveyDetailSerializer(serializers.ModelSerializer):

    # 多对多关系，需要指定子序列化器
    survey_templates = serializers.ListSerializer(child=SurveyTemplateSerializer())

    class Meta:
        model = models.Survey
        fields = (
            "id",
            "name",
            "survey_templates",
        )


# 创建的序列化器，创建需要进行数据校验，区分开
class SurveyCreateSerializer(serializers.ModelSerializer):
    # 多对多关系，需要指定子序列化器
    survey_templates = serializers.ListSerializer(child=SurveyTemplateSerializer())
    unique_code = serializers.CharField(required=True)

    class Meta:
        model = models.Survey
        fields = (
            "survey_templates",
            "unique_code"
        )

    # 局部钩子函数，判断唯一码是否已经使用过了
    def validate_unique_code(self, attrs):
        survey = self.context.get("view").kwargs["pk"]
        code = models.SurveyCode.objects.filter(unique_code=attrs, is_used=False, survey=survey).first()
        if not code:
            raise serializers.ValidationError("无效的唯一码")
        return code

