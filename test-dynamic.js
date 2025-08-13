// Test script to demonstrate dynamic menu generation
const testItems = [
  'Chicken Biryani',
  'Margherita Pizza', 
  'Veggie Burger',
  'Chocolate Cake',
  'Mango Smoothie',
  'Paneer Tikka',
  'Sushi Roll'
];

async function testDynamicGeneration() {
  console.log('🧪 Testing Dynamic Menu Generation\n');
  
  for (const item of testItems) {
    try {
      const response = await fetch('http://localhost:4000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ itemName: item, simulate: true })
      });
      
      const data = await response.json();
      
      console.log(`🍽️  ${item}:`);
      console.log(`   Description: ${data.description}`);
      console.log(`   Upsell: ${data.combos[0]}`);
      console.log('');
      
    } catch (error) {
      console.error(`❌ Error testing ${item}:`, error.message);
    }
  }
}

// Run the test
testDynamicGeneration();
