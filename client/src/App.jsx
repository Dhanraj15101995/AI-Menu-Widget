import React, { useState } from 'react'
import MenuForm from './components/MenuForm'
import Suggestions from './components/Suggestions'

export default function App() {
  const [description, setDescription] = useState('')
  const [upsellSuggestion, setUpsellSuggestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [generatedAt, setGeneratedAt] = useState('')
  const [modelUsed, setModelUsed] = useState('')

  const handleGenerate = async (itemName, simulate = false, gptModel = 'gpt-3.5-turbo') => {
    setError('')
    setLoading(true)
    try {
      const res = await fetch('http://localhost:4000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          itemName: itemName, 
          simulate
        })
      })
      
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: 'Server error' }))
        throw new Error(errorData.detail || `HTTP ${res.status}`)
      }
      
      const data = await res.json()
      setDescription(data.description || '')
      setUpsellSuggestion(data.combos?.[0] || '')
      setGeneratedAt(new Date().toISOString())
      setModelUsed(simulate ? 'simulate' : 'gpt-3.5-turbo')
    } catch (err) {
      setError(err.message)
      setDescription('')
      setUpsellSuggestion('')
      setGeneratedAt('')
      setModelUsed('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>🍽️ AI Menu Intelligence Widget</h1>
        <p className="sub">Transform any food item into an irresistible menu description with smart upsell suggestions</p>
      </header>

      <MenuForm onGenerate={handleGenerate} loading={loading} />
      
      {error && (
        <div className="error">
          <strong>⚠️ Error:</strong> {error}
        </div>
      )}
      
      <Suggestions 
        description={description} 
        upsellSuggestion={upsellSuggestion}
        generatedAt={generatedAt}
        modelUsed={modelUsed}
      />
    </div>
  )
}


