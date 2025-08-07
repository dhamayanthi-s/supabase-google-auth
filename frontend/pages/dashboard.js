import { useEffect, useState } from 'react'
import { supabase } from '../utils/supabaseClient'

export default function Dashboard() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const fetchUser = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      const user = session.user
      setUser(user)

      await fetch('http://localhost:5000/api/save-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({
          email: user.email,
          name: user.user_metadata.full_name
        })
      })
    }

    fetchUser()
  }, [])

  if (!user) return <p>Loading user...</p>

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome, {user.user_metadata.full_name}!</h1>
      <p>Email: {user.email}</p>
    </div>
  )
}