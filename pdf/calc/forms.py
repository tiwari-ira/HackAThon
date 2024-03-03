from django import forms

class SuccessPredictionForm(forms.Form):
    APPLICATION_TYPE = forms.CharField(label="APPLICATION_TYPE")
    AFFILIATION = forms.CharField(label="AFFILIATION")
    CLASSIFICATION = forms.CharField(label="CLASSIFICATION")
    USE_CASE = forms.CharField(label="USE_CASE")
    ORGANIZATION = forms.CharField(label="ORGANIZATION")
    STATUS = forms.CharField(label='STATUS')
    INCOME_AMT = forms.CharField(label='INCOME_AMT')
    SPECIAL_CONSIDERATIONS = forms.CharField(label='SPECIAL_CONSIDERATIONS')
    ASK_AMT = forms.CharField(label='ASK_AMT')
