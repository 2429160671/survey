# Generated by Django 2.2.6 on 2020-05-12 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='问卷名称')),
                ('times', models.PositiveSmallIntegerField(verbose_name='第几次问卷调查')),
                ('count', models.PositiveSmallIntegerField(verbose_name='生成多少唯一码')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ClassList', verbose_name='哪一个班级的')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=10, unique=True)),
                ('is_used', models.BooleanField(default=False, verbose_name='是否使用')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_type', models.CharField(choices=[('choice', '单选'), ('suggest', '建议')], max_length=32, verbose_name='问题类型')),
                ('title', models.CharField(max_length=64, verbose_name='问题标题')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='模板名称(哪个人员的)', max_length=64)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('questions', models.ManyToManyField(to='web.SurveyQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='分数')),
                ('content', models.CharField(blank=True, max_length=1024, null=True, verbose_name='建议')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.SurveyChoice', verbose_name='问题的选项')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.SurveyQuestion', verbose_name='哪一个问题')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Survey', verbose_name='那一次问卷调查')),
                ('survey_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.SurveyCode')),
                ('survey_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.SurveyTemplate', verbose_name='哪一个角色的')),
            ],
        ),
        migrations.AddField(
            model_name='surveychoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.SurveyQuestion', verbose_name='关联问题'),
        ),
        migrations.AddField(
            model_name='survey',
            name='survey_templates',
            field=models.ManyToManyField(to='web.SurveyTemplate', verbose_name='针对哪几个角色的问卷调查'),
        ),
    ]
