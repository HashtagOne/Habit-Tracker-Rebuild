import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import { isLoggedIn, authReady } from '../auth.js'
import { watch } from 'vue'

const router = createRouter({
    history: createWebHistory('/Habit-Tracker-Rebuild/'),
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

router.beforeEach(async (to, from, next) => {
    // wait for auth check to complete before making any routing decisions
    if (!authReady.value) {
        await new Promise(resolve => {
            const stop = watch(authReady, (val) => {
                if (val) {
                    stop()
                    resolve()
                }
            })
        })
    }

    if (to.meta.requiresAuth && !isLoggedIn.value) {
        next('/login')
    } else {
        next()
    }
})


export default router