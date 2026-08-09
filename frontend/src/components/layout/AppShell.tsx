import { Outlet } from 'react-router-dom'
import { TopNav } from './TopNav'
import { Footer } from './Footer'

export function AppShell() {
  return (
    <div className="min-h-screen bg-paper flex flex-col justify-between">
      <div>
        <TopNav />
        <main>
          <div className="mx-auto max-w-7xl px-4 py-6 md:px-8 md:py-8">
            <Outlet />
          </div>
        </main>
      </div>
      <Footer />
    </div>
  )
}
