import React, { useState } from 'react'

export default function MenuForm({ onGenerate, loading }) {
  const [item, setItem] = useState('')
  const [simulate, setSimulate] = useState(false)
  const [gptModel, setGptModel] = useState('gpt-3.5-turbo')

  const submit = (e) => {
    e.preventDefault()
    if (!item.trim()) return
    onGenerate(item.trim(), simulate, gptModel)
  }

  const examples = [
    'Paneer Tikka Pizza',
    'Chicken Biryani',
    'Margherita Pizza',
    'Butter Chicken',
    'Veggie Burger',
    'Chocolate Cake',
    'Mango Smoothie'
  ]

  const handleExampleClick = (example) => {
    setItem(example)
  }

  return (
    <div className="menu-form-container">
      <form onSubmit={submit} className="menu-form">
        <input
          value={item}
          onChange={(e) => setItem(e.target.value)}
          placeholder='e.g., "Paneer Tikka Pizza", "Chicken Biryani", "Margherita Pizza"'
          aria-label="Food item"
          className="menu-input"
        />
        <div className="form-controls">
          <div className="control-group">
            <label className="simulate">
              <input type="checkbox" checked={simulate} onChange={(e) => setSimulate(e.target.checked)} />
              Simulate (no API)
            </label>

            {/* Bonus: GPT Model Toggle */}
            {!simulate && (
              <label className="model-selector">
                <span>GPT Model:</span>
                <select
                  value={gptModel}
                  onChange={(e) => setGptModel(e.target.value)}
                  className="model-select"
                >
                  <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Fast)</option>
                  <option value="gpt-4">GPT-4 (Premium)</option>
                </select>
              </label>
            )}
          </div>

          <button type="submit" disabled={loading} className="generate-btn">
            {loading ? (
              <>
                <span className="loading"></span>
                Generating...
              </>
            ) : (
              'Generate Menu Description'
            )}
          </button>
        </div>
      </form>

      <div className="examples">
        <p className="examples-title">Try these examples:</p>
        <div className="example-buttons">
          {examples.map((example, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleExampleClick(example)}
              className="example-btn"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
