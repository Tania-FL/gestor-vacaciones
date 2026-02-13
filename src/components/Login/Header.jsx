import logoCDMX from '../../images/logo-header.png';
import logoLlave from '../../images/logo-llave-exp.png';

export default function Header() {
    return (
        <header className="w-full bg-white border-b">
            <div className="w-full flex items-center justify-between px-1 py-0.5">
                <div className="flex items-center gap-3 px-6 py-3">
                    <img src={logoCDMX} alt="Logo Gobierno de la Ciudad de Mexico 2024 - 2030" className="h-14" />
                </div>

                <button className='flex items-center gap-3 px-6 py-3 text-sm font-medium text-purple-700 border-2 border-gray-200 rounded-md hover:bg-gray-50 transition'>
                    Ingresa a tu
                    <img src={logoLlave} alt="Logo Llave CDMX" className='h-6' />
                </button>
            </div>
        </header>
    )
}