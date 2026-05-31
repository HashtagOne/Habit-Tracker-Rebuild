<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { isLoggedIn, currentUsername, authReady} from './auth.js'


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
    <div class="app-wrapper">
        <RouterView v-slot=" {Component}">
            <Transition name="page" appear>
                <component :is="Component" :key="$route.path" />
            </Transition>
        </RouterView>
    </div>
</template>

<style>
.app-wrapper {
    position: relative;
    min-height: 100vh;
}

.page-leave-active {
    background: red !important;
    transition: opacity 0.5s ease;
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 10;
}

.page-enter-active {
    transition: opacity 0.5s ease;
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
}
.page-enter-from,
.page-leave-to {
    opacity: 0;
}
</style>