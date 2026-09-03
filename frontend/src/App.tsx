import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import { ToastProvider } from '@/context/ToastContext'
import { ThemeProvider } from '@/context/ThemeContext'
import { ProtectedRoute } from '@/routes/ProtectedRoute'
import { AppShell } from '@/components/layout/AppShell'
import Login from '@/pages/auth/Login'
import Register from '@/pages/auth/Register'
import Dashboard from '@/pages/Dashboard'
import Transactions from '@/pages/transactions/Transactions'
import Budgets from '@/pages/Budgets'
import Analytics from '@/pages/Analytics'
import Insights from '@/pages/Insights'
import Assistant from '@/pages/Assistant'
import Recurring from '@/pages/Recurring'
import Receipts from '@/pages/Receipts'
import ExportPage from '@/pages/Export'

import About from '@/pages/About'

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <ToastProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              <Route
                element={
                  <ProtectedRoute>
                    <AppShell />
                  </ProtectedRoute>
                }
              >
                <Route path="/" element={<Dashboard />} />
                <Route path="/transactions" element={<Transactions />} />
                <Route path="/budgets" element={<Budgets />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/insights" element={<Insights />} />
                <Route path="/assistant" element={<Assistant />} />
                <Route path="/recurring" element={<Recurring />} />
                <Route path="/receipts" element={<Receipts />} />
                <Route path="/export" element={<ExportPage />} />
                <Route path="/about" element={<About />} />
              </Route>

              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </ToastProvider>
      </AuthProvider>
    </ThemeProvider>
  )
}
