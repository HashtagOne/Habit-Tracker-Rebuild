<script setup>
import {ref, onMounted} from 'vue'
import ModalOverlay from './ModalOverlay.vue'
import ConfirmOverlay from './ConfirmOverlay.vue'


const editingId = ref(null)
const editingName = ref("")

const modalVisible = ref(false)
const modalHeading = ref("")
const modalInitialValue = ref("")
const modalCallback = ref(null)
const modalPlaceholder = ref("")
const modalAccentColor = ref("#3B6D11")

const confirmVisible = ref(false)
const confirmHeading = ref("")
const confirmCallback = ref(null)

function startEdit(category) {
    editingId.value = category.id
    editingName.value = category.name
}

async function saveEdit(id) {
    await fetch(`${API}/categories/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        credentials: "include",
        body: JSON.stringify({name: editingName.value})
    })

    editingId.value = null
    emit('updated')
}

const props = defineProps({
    categories: {
        type: Array,
        default: () => []
    },
    selectedId: {
        type: Number,
        default: null
    }
})

const emit = defineEmits(['select', 'updated'])

const API = "http://localhost:5000"

const colors = ["forest", "sage", "amber", "terracotta", "slate"]
let colorIndex = 0

function nextColor() {
    const color = colors[colorIndex % colors.length]
    colorIndex++
    return color
}

function addCategory() {
    const color = colors[colorIndex % colors.length]
    modalAccentColor.value = `var(--color-${color})`
    modalHeading.value = "Add Category"
    modalInitialValue.value = ""
    modalVisible.value = true
    modalPlaceholder.value = "e.g. Morning Routine"
    modalCallback.value = async (name) => {
        
        const color = nextColor()

        await fetch(`${API}/categories`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            credentials: "include",
            body: JSON.stringify({name, color})
        })

        emit('updated')
    }
}

function handleSave(value) {
    if (modalCallback.value) modalCallback.value(value)
    modalVisible.value = false
}

function handleCancel() {
    modalVisible.value = false
}

function deleteCategory(e, id) {
    e.stopPropagation()

    confirmHeading.value = "Delete this category?"
    confirmVisible.value = true
    confirmCallback.value = async () => {

        await fetch(`${API}/categories/${id}`, {
            method: "DELETE",
            credentials: "include"
        })
        emit('updated')
    }
}

function handleConfirm() {
    if (confirmCallback.value) confirmCallback.value()
    confirmVisible.value = false
}

function handleConfirmCancel() {
    confirmVisible.value = false
}

function selectCategory(category) {
    emit('select', category)
}
</script>

<template>
    <aside class="sidebar">
        <div class="sidebar-header">
            <span class="sidebar-label">Categories</span>
        </div>

        <div class="categories-list">
            <div
                v-for="category in categories"
                :key="category.id"
                class="category-item"
                :class="[`color-${category.color}`, { active: category.id === selectedId }]"
                :style="{ '--category-color': `var(--color-${category.color})` }"
                @click="selectCategory(category)"
            >
                <div class="category-info">
                    <span
                        v-if="editingId !== category.id"
                        class="category-name" 
                        @dblclick="startEdit(category)">
                        {{ category.name }}</span>

                    <input
                        v-else
                        class="edit-input"
                        v-model="editingName"
                        @keydown.enter="saveEdit(category.id)"
                        @blur="saveEdit(category.id)"
                        @click.stop
                    />
                    <span class="category-count">{{ category.habits.length }} habits</span>
                </div>
                <button
                    class="delete-category-btn"
                    @click="deleteCategory($event, category.id)"
                >✕</button>
            </div>

            <p v-if="categories.length === 0" class="empty-state">
                No categories yet.
            </p>
        </div>

        <button class="add-category-btn" @click="addCategory">
            + Add Category
        </button>

        <ModalOverlay
            :visible="modalVisible"
            :heading="modalHeading"
            :accentColor="modalAccentColor"
            :initialValue="modalInitialValue"
            :placeholder="modalPlaceholder"
            @save="handleSave"
            @cancel="handleCancel"
        />
        <ConfirmOverlay
            :visible="confirmVisible"
            :heading="confirmHeading"
            @confirm="handleConfirm"
            @cancel="handleConfirmCancel"
        />
    </aside>
</template>

<style scoped>
.sidebar {
    height: 100%;
    background: var(--bg-sidebar);
    border-right: 0.5px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-height: 0;
}

.sidebar-header {
    padding: 20px 16px 12px;
    border-bottom: 0.5px solid var(--border);
}

.sidebar-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}

.categories-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.category-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    border-left: 3px solid transparent;
    border-top: 0.5px solid transparent;
    border-bottom: 0.5px solid transparent;
    border-right: 4px solid transparent;
    transition: background-color 0.2s, border-color 0.2s;
    animation: slideInFromLeft 0.5s ease-out both;
}

.category-item:hover {
    background-color: var(--bg-card);
    border-top-color: var(--border);
    border-bottom-color: var(--border);
    border-right-color: var(--border);
}

.category-item:active {
    background-color: var(--bg-card);
}

.edit-input {
    background: transparent;
    border: none;
    border-bottom: 1px solid var(--category-color);
    outline: none;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
    width: 100%;
    padding: 0;
}

.color-forest {border-left-color: var(--color-forest); }
.color-forest.active { 
    border-top-color: var(--color-forest);
    border-bottom-color: var(--color-forest);
    border-right-color: var(--color-forest);
}
.color-sage {border-left-color: var(--color-sage); }
.color-sage.active { 
    border-top-color: var(--color-sage);
    border-bottom-color: var(--color-sage);
    border-right-color: var(--color-sage);
}
.color-amber {border-left-color: var(--color-amber); }
.color-amber.active { 
    border-top-color: var(--color-amber);
    border-bottom-color: var(--color-amber);
    border-right-color: var(--color-amber);
}
.color-terracotta {border-left-color: var(--color-terracotta); }
.color-terracotta.active { 
    border-top-color: var(--color-terracotta);
    border-bottom-color: var(--color-terracotta);
    border-right-color: var(--color-terracotta);
}
.color-slate {border-left-color: var(--color-slate); }
.color-slate.active { 
    border-top-color: var(--color-slate);
    border-bottom-color: var(--color-slate);
    border-right-color: var(--color-slate);
}

.color-forest.active .category-name { color: var(--color-forest); }
.color-sage.active .category-name { color: var(--color-sage); }
.color-amber.active .category-name { color: var(--color-amber); }
.color-terracotta.active .category-name { color: var(--color-terracotta); }
.color-slate.active .category-name { color: var(--color-slate); }

.category-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.95rem;
}

.category-name {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
    transition: color 0.2s;
}

.category-count {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.delete-category-btn {
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 0.75rem;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s;
    padding: 2px 6px;
}

.category-item:hover .delete-category-btn {
    opacity: 0.9;
}

.empty-state {
    font-size: 0.85rem;
    color: var(--text-muted);
    padding: 16px;
    text-align: center;
}

.add-category-btn {
    margin: 8px;
    margin-bottom: 24px;
    padding: 10px;
    background: transparent;
    border: 0.5px solid var(--border);
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
}

.add-category-btn:hover {
    border-color: var(--accent-green);
    color: var(--accent-green);
}

@keyframes slideInFromLeft {
    from {
        opacity: 0;
        transform: translateX(-24px);
    }
    to {
        opacity: 1;
        transform: translateX(0)
    }
}

</style>