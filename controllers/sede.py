from models.sedeLibro import SedeLibroModel
from flask_restful import Resource, reqparse
from models.sede import SedeModel
# basico
# get all sede
# create sede
# vincula una sede con varios libros y viceversa (un libro con varias sedes)
serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    location='json',
    dest='latitud'
)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required=True,
    help='Fata la sede_ubicacion',
    location='json',
    dest='ubicacion'
)
serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    location='json',
    dest='longitud' # es como se va a llamar una vez que hemos usado el metodo parse_args()
)
class SedesController(Resource):
    def post(self):
        data = serializer.parse_args()
        print(data)
        # LOS TIPOS DE DATOS QUE NO SON NI NUMERICOS NI STRINGS = DECIMAL, FECHA, NO PUEDE HACER LA CONVERSION AUTOMATICA
        nuevaSede = SedeModel(data['ubicacion'],data['latitud'], data['longitud'])
        nuevaSede.save()
        return {
            'success': True,
            'content': nuevaSede.json(),
            'message': 'Se creo la sede exitosamente'
        }, 201
    def get(self):
        sedes = SedeModel.query.all()
        resultado = []
        for sede in sedes:
            resultado.append(sede.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }



# busqueda de todos los libros de una sede 
class LibroSedeController(Resource):
    def get(self, id_sede):
        # de acuerdo al id de la sede, devolver todos los libros que hay en esa sede.
        sede = SedeModel.query.filter_by(sedeId = id_sede).first()
        # SedeLibroModel.query.filter_by(sedeId = id_sede).first()
        sedeLibros = sede.libros # todas mis sedelibros
        libros=[]
        for sedeLibro in sedeLibros:
            libro = sedeLibro.libroSede.json()
            # agregar el autor de ese libro
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
            # agregar la categoria del libro pero solamente su descripcion (no necesito el ID)
            # print(sedeLibro.libroSede.categoriaLibro.categoriaDescripcion)
            libro['categoria'] = sedeLibro.libroSede.categoriaLibro.json()
            del libro['categoria']['categoria_id']
            del libro['autor_id']
            libros.append(libro)
            
        resultado = sede.json()
        resultado['libros'] = libros
        return {
            'success':True,
            'content': resultado
        }




# busqueda de todos los libros de una sede segun su categoria
# categoria
# sede
# 127.0.0.1:5000/buscarLibroCategoria?sede=1&categoria=2
class LibroCategoriaSedeController(Resource):
    def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.remove_argument('sede_longitud')
        serializer.add_argument(
            'categoria',
            type=int,
            required=True,
            help='Falta la categoria',
            location='args'
        )
        serializer.add_argument(
            'sede',
            type=int,
            required=True,
            help='Falta la sede',
            location='args' # sirve para que me lo mande por el querystring (de forma dinamica)
        )
        data = serializer.parse_args()
        # luego de mi sede ingresar a mi sede_libro -> [] ... , luego ingresar a mis libros y hacer el filtro segun la categoria (data['categoria'])
        sede = SedeModel.query.filter_by(sedeId = data['sede']).first()
        # print(sede.libros)
        libros = []
        for sedelibro in sede.libros:
            # print(sedelibro.libroSede.categoria)
            if (sedelibro.libroSede.categoria == data['categoria']):
                libros.append(sedelibro.libroSede.json())
                
        return {
            'success': True,
            'content': libros
        }