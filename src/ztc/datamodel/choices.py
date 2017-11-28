from djchoices import ChoiceItem, DjangoChoices


class JaNee(DjangoChoices):
    ja = ChoiceItem('J', 'Ja')
    nee = ChoiceItem('N', 'Nee')
