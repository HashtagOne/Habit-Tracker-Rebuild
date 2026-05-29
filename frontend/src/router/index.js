import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import { isLoggedIn } from '../auth.js'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/login',
            component: LoginView
        },
        {
            path: '/register',
            component: RegisterView
        },
        {
            path: '/',
            component: DashboardView,
            meta: { requiresAuth: true }
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !isLoggedIn.value) {
        next('/login')
    } else {
        next()
    }
})


export default router