import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// assets 폴더에 있는 스타일 시트 임포트
import './assets/style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
