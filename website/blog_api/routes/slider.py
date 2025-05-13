from ninja import Router # type: ignore

router = Router(
    tags=['Slider']
)

@router.get('/slider/')
def get_slider_item(request):
    return ['slider']
