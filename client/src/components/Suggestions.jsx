import React from 'react'

export default function Suggestions({ description, upsellSuggestion, generatedAt, modelUsed }) {
  if (!description && !upsellSuggestion) {
    return (
      <div className="empty">
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🍕</div>
        <div>No results yet — enter a food item and click Generate to see the magic!</div>
      </div>
    )
  }

  const formatDateTime = (dateString) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleString()
    } catch {
      return dateString
    }
  }

  const getModelDisplayName = (model) => {
    switch (model) {
      case 'gpt-3.5-turbo':
        return 'GPT-3.5 Turbo'
      case 'gpt-4':
        return 'GPT-4'
      case 'simulate':
        return 'Simulation Mode'
      case 'fallback':
        return 'Fallback Mode'
      default:
        return model || 'Unknown'
    }
  }

  return (
    <div className="results">
      {description && (
        <div className="card success-animation">
          <h3>Menu Description</h3>
          <p>{description}</p>
          {generatedAt && (
            <div className="meta-info">
              <small>Generated: {formatDateTime(generatedAt)}</small>
              {modelUsed && <small> • Model: {getModelDisplayName(modelUsed)}</small>}
            </div>
          )}
        </div>
      )}

      {upsellSuggestion && (
        <div className="card success-animation">
          <h3>Upsell Suggestion</h3>
          <p>{upsellSuggestion}</p>
        </div>
      )}
    </div>
  )
}
