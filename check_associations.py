from apps.finanzas.models import Datafono, CuentaBancariaEmpresa, MetodoPago

print('Datafonos:')
for d in Datafono.objects.all():
    metodos = list(d.metodos_pago.values_list('id_metodo_pago', 'nombre_metodo'))
    print(f'{d.nombre}: {metodos}')

print('\nCuentas bancarias:')
for c in CuentaBancariaEmpresa.objects.all():
    metodos = list(c.metodos_pago.values_list('id_metodo_pago', 'nombre_metodo'))
    print(f'{c.nombre_banco} {c.numero_cuenta}: {metodos}')

print('\nMétodos de pago disponibles:')
for m in MetodoPago.objects.all():
    print(f'{m.id_metodo_pago}: {m.nombre_metodo}')