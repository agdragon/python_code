# -*- coding: utf-8 -*-
    
import uuid

name = "test_name"
namespace = "test_namespace"

print uuid.uuid1() # ���εķ����μ�Python Doc
print uuid.uuid3(namespace, name)
print uuid.uuid4()
print uuid.uuid5(namespace, name)