from django.contrib import admin
from .models import User,CodeType,Plan,Productcategory,Product,ProductInventory,Code,Codeapply

admin.site.register(User),
admin.site.register(CodeType),
admin.site.register(Plan),
admin.site.register(Productcategory),
admin.site.register(Product),
admin.site.register(ProductInventory),
admin.site.register(Code),
admin.site.register(Codeapply),