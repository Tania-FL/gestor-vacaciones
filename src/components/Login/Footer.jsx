import facebook from '../../images/facebook.png'
import x from '../../images/xlogo.png'
import datosAbiertos from '../../images/grupo.png'

export default function Footer() {
    return (
        <footer className="bg-white border-t">
            <div className="max-w-7xl mx-auto px-6 py-6 grid md:grid-cols-3 gap-6 text-sm items-center">
                <div>
                    <p>Para emergencias, <br />marca <strong>911</strong></p>
                    <p>Dudas e informacion, <br />marca <strong>*0311</strong></p>
                </div>

                <div className="flex items-center gap-4 justify-center">
                    <img src={facebook} alt="Facebook" className="h-6" />
                    <img src={x} alt="X" className="h-6" />
                </div>

                <div className="flex justify-end">
                    <img src={datosAbiertos} alt="Portal de Datos Abiertos" className="h-30" />
                </div>
            </div>
        </footer>
    )
}