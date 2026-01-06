import { createBrowserRouter } from 'react-router-dom'
import App from '../App'
import AdminPanel from '../components/AdminPanel'

// Define application routes
const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
  },
  {
    path: '/admin',
    element: <AdminPanel />,
  },
])

export default router
