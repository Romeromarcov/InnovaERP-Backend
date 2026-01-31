from apps.finanzas.models import Datafono, CuentaBancariaEmpresa
from apps.finanzas.serializers import DatafonoSerializer, CuentaBancariaEmpresaSerializer
import json

d = Datafono.objects.first()
if d:
    ds = DatafonoSerializer(d)
    print('Datafono fields:')
    print(json.dumps(ds.data, indent=2))

c = CuentaBancariaEmpresa.objects.first()
if c:
    cs = CuentaBancariaEmpresaSerializer(c)
    print('CuentaBancaria fields:')
    print(json.dumps(cs.data, indent=2))