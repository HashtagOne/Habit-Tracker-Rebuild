<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isLoggedIn, currentUsername, transitionName } from '../auth.js'
import CategorySidebar from '../components/CategorySidebar.vue'
import HabitsPanel from '../components/HabitsPanel.vue'
import { API } from '../config.js'

const router = useRouter()

const categories = ref([])
const selectedCategory = ref(null)
const loading = ref(true)

async function loadCategories() {
    try {
        const response = await fetch(`${API}/categories`, {
            credentials: "include"
        })

        if (response.status === 401) {
            isLoggedIn.value = false
            router.push("/login")
            return
        }

        const data = await response.json()
        categories.value = data

        if (selectedCategory.value) {
            const updated = data.find(c => c.id === selectedCategory.value.id)
            selectedCategory.value = updated || null
        }
    } catch (err) {
        console.error("Failed to load categories", err)
    } finally {
        loading.value = false
    }
}

async function logout() {
    await fetch(`${API}/auth/logout`, {
        method: "POST",
        credentials: "include"
    })
    isLoggedIn.value = false
    currentUsername.value = ""
    transitionName.value = 'fade-down'
    router.push("/login")
}

function selectCategory(category) {
    selectedCategory.value = category
}

onMounted(() => {
    loadCategories()
})
</script>



<template>
    <div class="dashboard">
        <header class="dashboard-header">
            <h1 class="dashboard-title">Habits</h1>
            <div class="header-right">
                <span class="username">{{  currentUsername }}</span>
                <button class="logout-btn" @click="logout">Log Out</button>
            </div>
        </header>

        <div class="dashboard-body">
            <CategorySidebar
                :categories="categories"
                :selectedId="selectedCategory?.id ?? null"
                @select="selectCategory"
                @updated="loadCategories"
            />
            <HabitsPanel
                :category="selectedCategory"
                @updated="loadCategories"
            />
        </div>
    </div>
</template>

<style scoped>


.dashboard {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}

.dashboard-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-bottom: 0.5px solid var(--border);
    background: var(--bg-primary);
    flex-shrink: 0;
}

.dashboard-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
}

.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.username {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.logout-btn {
    background: transparent;
    border: 0.5px solid var(--border);
    border-radius: 8px;
    padding: 6px 14px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
}

.logout-btn:hover {
    border-color: var(--accent-amber);
    color: var(--accent-amber);
}

.dashboard-body {
    display: grid;
    grid-template-columns: 280px 1fr;
    flex: 1;
    overflow: hidden;
    min-height: 0;
}
</style>