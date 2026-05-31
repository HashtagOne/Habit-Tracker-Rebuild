<script setup>
import { computed } from 'vue'

const props = defineProps({
    category: {
        type: Object,
        default: []
    }
})

const emit = defineEmits(['updated'])

const API = "http://localhost:5000"

// today's date in YYYY-MM-DD format
const today = new Date().toISOString().split("T")[0]

// checks if habit has a completion for today
function isCompletedToday(habit) {
    return habit.completions.some(c => c.date === today)
} 

// finds completion id for today so it can be deleted on uncheck
function todayCompletionId(habit) {
    const completion = habit.completions.find(c => c.date === today)
    return completion ? completion.id : null
}

// calculates streakk for habit
function getStreak(habit) {
    let streak = 0
    let date = new Date()

    while (true) {
        const dateStr = date.toISOString().split("T")[0]
        if (habit.completions.some(c => c.date === dateStr)) {
            streak++
            date.setDate(date.getDate() - 1)
        } else {
            break
        }
    }
    return streak
}

async function toggleHabit(habit) {
    if (isCompletedToday(habit)) {
        // find the completion and delete it
        const completion = habit.completions.find(c => c.date === today)
        if (!completion) return

        await fetch(`${API}/completions/${completion.id}`, {
            method: "DELETE",
            credentials: "include" 
        })
    } else {
        await fetch(`${API}/completions`, {
            method: "POST",
            headers: { "Content-Type": "application/json"}, 
            credentials: "include",
            body: JSON.stringify({ habit_id: habit.id})
        })
    }
    emit('updated')
}

async function addHabit() {
    const name = prompt("Habit name:")
    if (!name) return

    await fetch(`${API}/habits`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        credentials: "include",
        body: JSON.stringify({
            name,
            category_id: props.category.id
        })
    })
    emit('updated')
}

async function deleteHabit(e, id) {
    e.stopPropagation() 

    await fetch(`${API}/habits/${id}`, {
        method: "DELETE",
        credentials: "include"
    })
    emit('updated')
}

const progress = computed(() => {
    if (!props.category || props.category.habits.length === 0) return 0
    const completed = props.category.habits.filter(h => isCompletedToday(h)).length
    return Math.round((completed / props.category.habits.length) * 100)
})
</script>

<template>
    <div class="habit-panel">

        <!-- empty state -->
         <div v-if="!category" class="no-selection">
            <p> Select a category to view the habits inside.</p>
         </div>

         <!-- habit panel when there's a category -->
          <div v-else class="panel-content" :style="{'--category-color': `var(--color-${category.color})`}">
            <div class="panel-header">

                <div class="panel-title">
                    <h2>{{  category.name  }}</h2>
                    <span class="progress-label"> {{  progress  }} % today </span>
                </div>
                <div class="progress-bar-track">
                    <div
                        class="progress-bar-fill"
                        :style ="{width: `${progress}%`}"
                    ></div>
                </div>
            </div>

            <div class="habits-list">
                <div
                    v-for="habit in category.habits"
                    :key="habit.id"
                    class="habit-row"
                >
                    <input
                        type="checkbox"
                        class="habit-checkbox"
                        :checked="isCompletedToday(habit)"
                        @change="toggleHabit(habit)"
                    />
                    <div class="habit-info">
                        <span class="habit-name">{{  habit.name  }}</span>
                        <span class="habit-streak">🔥 {{ getStreak(habit) }}</span>
                    </div>
                    <button
                        class="delete-habit-btn"
                        @click="deleteHabit($event, habit.id)"
                    >✕</button>
                </div>

                <p v-if="category.habits.length === 0" class="empty-habits">
                    No habits yet. How about adding one below?
                </p>
            </div>

            <button class="add-habit-btn" @click="addHabit">
                + Add Habit
            </button>
          </div>
    </div>
</template>

<style scoped>
.habit-panel {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg-primary);
}

.no-selection {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--text-muted);
    font-size: 0.9rem;
}

.panel-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 24px 32px;
    gap: 20px;
    animation: fadeSlideUp 0.9s ease-out both;
}

.panel-header {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.panel-title {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
}

.panel-title h2 {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
}

.progress-label {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.progress-bar-track {
    height: 4px;
    background: var(--border);
    border-radius: 99px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    background: var(--category-color);
    border-radius: 99px;
    transition: width 0.6s ease;
}

.habits-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
    overflow-y: auto;
}

.habit-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 0.5px solid var(--border);
    animation: fadeSlideUp 0.4s ease-out both;
}

.habit-row:last-child {
    border-bottom: none;
}

.habit-checkbox {
    appearance: none;
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid var(--border);
    flex-shrink: 0;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    background: transparent;
}

.habit-checkbox:checked {
    background-color: var(--category-color);
    border-color: var(--category-color);
}

.habit-checkbox:checked:after {
    content: "✓";
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 11px;
    width: 100%;
    height: 100%;
}

.habit-info {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.habit-name {
    font-size: 0.95rem;
    color: var(--text-primary);
}

.habit-streak {
    font-size: 0.8rem;
    color: var(--accent-amber);
}

.delete-habit-btn {
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 0.75rem;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s;
    padding: 2px 6px;
}

.habit-row:hover .delete-habit-btn {
    opacity: 0.9;
}

.empty-habits {
    font-size: 0.85rem;
    color: var(--text-muted);
    padding: 16px 0;
}

.add-habit-btn {
    background: transparent;
    border: 0.5px dashed var(--border);
    border-radius: 8px;
    padding: 10px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
    text-align: left;
}

.add-habit-btn:hover {
    border-color: var(--accent-green);
    color: var(--accent-green);
}

@keyframes fadeSlideUp {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}


</style>