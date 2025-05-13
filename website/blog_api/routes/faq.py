from ninja import Router # type: ignore
from blog_app.models import FAQ
from blog_api.schemas.faq import FaqSchema,FaqCreationSchema,FaqUpdateSchema,FaqDeleteSchema
from django.shortcuts import get_object_or_404
from typing import Union

router = Router(
    tags=['FAQ']
)

@router.get('/faqs/',response=list[FaqSchema])
def get_faqs(request):
    items = FAQ.objects.all()
    return items

@router.post('/faqs/',response=FaqSchema)
def create_faq(request, faq_data: FaqCreationSchema):
    faq = FAQ.objects.create(**faq_data.dict())
    return faq

@router.get('/faqs/{faq_id}', response=FaqSchema)
def get_faq_by_id(request, faq_id: int):
    faq = get_object_or_404(FAQ, pk=faq_id)
    return faq

@router.patch('/faqs/{faq_id}/update/',response=FaqSchema)
def update_faq_item(request,faq_id: int, data: FaqUpdateSchema):
    faq = get_object_or_404(FAQ,pk=faq_id)

    for key, value in data.dict().items():
        if not value:
            current_value = getattr(faq, key)
            
            setattr(faq, key, current_value)
        else:
            setattr(faq, key, value)

    faq.save()
    return faq

@router.delete('/faqs/{faq_id}/', response=Union[FaqDeleteSchema, dict[str, str]])
def delete_faq(request, faq_id: int):
    faq = get_object_or_404(FAQ,pk=faq_id)
    faq.delete()
    return{'is_deleted': True}


