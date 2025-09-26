import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate, Counter } from 'k6/metrics';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

// 📊 Custom metrics
const todoCreationDuration = new Trend('todo_creation_duration');
const todoUpdateDuration = new Trend('todo_update_duration');
const todoDeleteDuration = new Trend('todo_delete_duration');
const todoCreationSuccessRate = new Rate('todo_creation_success_rate');
const todoCreationFailures = new Counter('todo_creation_failures');

export const options = {
    stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 10 },
        { duration: '30s', target: 20 },
        { duration: '1m', target: 20 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<1000'],
        http_req_failed: ['rate<0.10'],
        todo_creation_duration: ['p(95)<2000'],
        todo_update_duration: ['p(95)<2000'],
        todo_delete_duration: ['p(95)<2000'],
        todo_creation_success_rate: ['rate>0.90'],
    },
};

export default function () {
    const baseUrl = __ENV.BASE_URL || 'http://localhost:5000';
    const params = {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'todo_api' },
    };

    // 🩺 Health check
    const healthResponse = http.get(`${baseUrl}/health`, { tags: { name: 'health' } });
    check(healthResponse, {
        'health check is 200': (r) => r.status === 200,
        'health check <500ms': (r) => r.timings.duration < 500,
    });

    // 📥 Get all todos
    const getResponse = http.get(`${baseUrl}/api/todos`, { tags: { name: 'getTodos' } });
    check(getResponse, {
        'get todos is 200': (r) => r.status === 200,
        'get todos returns array': (r) => {
            try {
                return Array.isArray(JSON.parse(r.body));
            } catch (e) {
                return false;
            }
        },
    });

    // ➕ Create a new todo
    const payload = JSON.stringify({
        title: `Perf Todo - VU ${__VU} - Iter ${__ITER}`,
        description: 'Perf test todo',
    });

    const createStart = Date.now();
    const postResponse = http.post(`${baseUrl}/api/todos`, payload, params);
    todoCreationDuration.add(Date.now() - createStart);
    todoCreationSuccessRate.add(postResponse.status === 201);
    if (postResponse.status !== 201) todoCreationFailures.add(1);

    check(postResponse, {
        'create todo is 201': (r) => r.status === 201,
        'create todo has id': (r) => {
            try {
                return JSON.parse(r.body).id !== undefined;
            } catch (e) {
                return false;
            }
        },
    });

    if (postResponse.status === 201) {
        const todoId = JSON.parse(postResponse.body).id;

        // ✏️ Update todo
        const updatePayload = JSON.stringify({ title: `Updated - VU ${__VU}`, completed: true });
        const updateStart = Date.now();
        const updateResponse = http.put(`${baseUrl}/api/todos/${todoId}`, updatePayload, { tags: { name: 'updateTodo' } });
        todoUpdateDuration.add(Date.now() - updateStart);

        check(updateResponse, {
            'update todo is 200': (r) => r.status === 200,
            'update todo completed': (r) => {
                try {
                    return JSON.parse(r.body).completed === true;
                } catch (e) {
                    return false;
                }
            },
        });

        // 🗑️ Delete todo
        const deleteStart = Date.now();
        const deleteResponse = http.del(`${baseUrl}/api/todos/${todoId}`, null, { tags: { name: 'deleteTodo' } });
        todoDeleteDuration.add(Date.now() - deleteStart);

        check(deleteResponse, { 'delete todo is 204': (r) => r.status === 204 });
    }

    sleep(1);
}

// 📊 Export test summary
export function handleSummary(data) {
    return {
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
        'k6-summary.json': JSON.stringify(data),
        'k6-summary.html': `
      <html>
        <head><title>K6 Report</title></head>
        <body><h1>📊 K6 Performance Test Summary</h1><pre>${textSummary(data, { indent: ' ' })}</pre></body>
      </html>
    `,
    };
}
