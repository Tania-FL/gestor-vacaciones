import './App.css'
import Footer from './components/Login/Footer'
import Header from './components/Login/Header'
import Login from './components/Login/Login'

function App() {
  return (
    <div className='flex flex-col min-h-screen'>
      <Header />
      <Login />
      <Footer />
    </div>
  )
}

export default App
