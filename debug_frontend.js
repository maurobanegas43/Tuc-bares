// Script de debug para probar la conexión del frontend
const API_URL = 'http://localhost:8000';

async function testConnection() {
    console.log('=== TEST DE CONEXIÓN ===');
    
    // Test 1: Health check
    try {
        console.log('\n1. Probando /health...');
        const healthRes = await fetch(`${API_URL}/health`);
        const healthData = await healthRes.json();
        console.log('✅ Health:', healthData);
    } catch (err) {
        console.error('❌ Error en /health:', err.message);
    }
    
    // Test 2: Get places
    try {
        console.log('\n2. Probando /places?limit=10...');
        const placesRes = await fetch(`${API_URL}/places?limit=10`);
        const placesData = await placesRes.json();
        console.log(`✅ Places: ${placesData.length} lugares obtenidos`);
        console.log('Primer lugar:', placesData[0]);
    } catch (err) {
        console.error('❌ Error en /places:', err.message);
    }
    
    // Test 3: Chat status
    try {
        console.log('\n3. Probando /chat/status...');
        const chatRes = await fetch(`${API_URL}/chat/status`);
        const chatData = await chatRes.json();
        console.log('✅ Chat status:', chatData);
    } catch (err) {
        console.error('❌ Error en /chat/status:', err.message);
    }
}

testConnection();
