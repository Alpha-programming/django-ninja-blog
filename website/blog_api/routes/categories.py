from django.http import HttpRequest
from ninja import Router # type: ignore
from blog_api.schemas.categories import CategorySchema,CategoryCreationSchema
from blog_app.models import Category
from django.shortcuts import get_object_or_404
from slugify import slugify # type: ignore

router = Router(
    tags=['Categories']
)

@router.get('/categories/',response=list[CategorySchema])
def get_categories(request: HttpRequest):
    categories = Category.objects.all()
    return categories

@router.post('/categories/',response=CategorySchema)
def create_category(request, category_data: CategoryCreationSchema):
    category = Category.objects.create(
        name=category_data.name,
        slug=slugify(category_data.name)
    )
    return category

@router.get('/categories/{category_id}', response=CategorySchema)
def get_categories_by_id(request, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    return category

# @router.get('/categories/{category_slug}',response=CategorySchema)
# def get_categories_by_slug(request, category_slug: str):
#     '''Get category object by slug.'''
#     category = get_object_or_404(Category, slug=category_slug)
#     return category