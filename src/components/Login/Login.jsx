import bgLila from '../../images/iniciar_sesion.jpg'
import logoLlave from '../../images/logo-llave-exp.png'

export default function Login() {
    return (
        <main className="flex items-center justify-center bg-cover bg-center px-4 py-16" style={{ backgroundImage: `url(${bgLila})` }}>
            <div className='bg-white rounded-xl shadow-xl w-full max-w-md p-8'>
                <h1 className='text-center text-xl font-semibold text-gray-800 mb-4'>
                    Sistema de Gestion de Vacaciones
                </h1>

                <div className='flex justify-center mb-6'>
                    Inicia sesion con
                    <br />
                    <img src={logoLlave} alt="Llave CDMX" className='h-8' />
                </div>

                <form className='space-y-4'>
                    <div>
                        <label className='text-sm text-gray-600'>
                            Correo electronico o telefono
                        </label>
                        <input type="text" className='w-full mt-1 px-3 py-2 border rounded-md focus:outline-none focus: ring-2 focus: ring-purple-600' placeholder='Ingresa tu correo o telefono' />
                        <p className='text-right text-xs text-purple-700 mt-1 cursor-pointer'>
                            Olvide mi correo o telefono
                        </p>
                    </div>

                    <div>
                        <label className='text-sm text-gray-600'>
                            Contraseña
                        </label>
                        <input type="password" className='w-full mt-1 px-3 py-2 border rounded-md focus: outline-none focus: ring-2 focus: ring-purple-600' placeholder='Ingresa tu contraseña' />
                        <p className='text-right text-xs text-purple-700 mt-1 cursor-pointer'>
                            Olvide mi contraseña
                        </p>
                    </div>

                    <button type='button' className='w-full bg-purple-700 text-white py-2 rounded-md font-semibold hover:bg-purple-800 transition'>
                        Iniciar Sesion
                    </button>
                </form>

                <div className='text-center mt-6'>
                    <p className='text-sm text-gray-600'>¿No tienes cuenta?</p>
                    <button className='mt-2 w-full border border-purple-700 text-purple-700 py-2 rounded-md hover:bg-purple-50 transition'>
                        Crear cuenta
                    </button>
                </div>
            </div>
        </main>
    )
}