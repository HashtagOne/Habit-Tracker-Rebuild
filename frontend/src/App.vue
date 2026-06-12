<script setup>
import { RouterView, useRoute } from 'vue-router'
import { onMounted, ref, watch } from 'vue'
import { isLoggedIn, currentUsername, authReady } from './auth.js'

const route = useRoute()
const transitionName = ref('fade-up')

watch(() => route.path, (newPath) => {
    if (newPath === '/') {
        transitionName.value = 'fade-up'
    } else {
        transitionName.value = 'fade-down'
    }
})

onMounted(async () => {
    try {
        const response = await fetch("http://localhost:5000/auth/me", {
            credentials: "include"
        })
        if (response.ok) {
            const data = await response.json()
            isLoggedIn.value = true
            currentUsername.value = data.username
        } else {
            isLoggedIn.value = false
        }
    } catch (err) {
        isLoggedIn.value = false
    } finally {
        authReady.value = true
    }
})
</script>

<template>
    <div v-if="!authReady" class="auth-loading"></div>
    <div v-else class="router-wrapper">
        <RouterView v-slot="{ Component }">
            <Transition :name="transitionName">
                <component :is="Component" :key="$route.path" />
            </Transition>
        </RouterView>
    </div>
</template>

<style>
/* login → dashboard: fade up */
.router-wrapper {
    position: relative;
    min-height: 100vh;
    overflow: hidden;
}
.auth-loading {
    min-height: 100vh;
    background-color: var(--bg-primary);
}

.fade-up-enter-active,
.fade-down-enter-active {
    transition: opacity 1s ease, transform 1s ease;
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 1;
}

.fade-up-leave-active,
.fade-down-leave-active {
    transition: opacity 1s ease, transform 1s ease;
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 2;
}

.fade-up-enter-from { opacity: 0; transform: translateY(16px); }
.fade-up-leave-to { opacity: 0; transform: translateY(-16px); }
.fade-down-enter-from { opacity: 0; transform: translateY(-16px); }
.fade-down-leave-to { opacity: 0; transform: translateY(16px); }
</style>