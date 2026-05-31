<script setup>
import { ref, watch } from 'vue'
const inputValue = ref("")
const props = defineProps({
    visible: {
        type: Boolean,
        default: false
    },
    heading: {
        type: String,
        default: ""
    }, 
    initialValue: {
        type: String,
        default: ""
    },
    placeholder: {
        type: String,
        default: "Type here.."
    },
    accentColor: {
        type: String,
        default: "#3B6D11"
    }
})

const emit = defineEmits(['save','cancel'])

watch(() => props.visible, (val) => {
    if (val) {
        inputValue.value = props.initialValue
    }
})
</script>

<template>
    <Transition name="modal">
        <div class="modal-overlay" v-if="visible" @click.self="emit('cancel')">
            <div class="modal-card" :style="{ '--modal-accent': accentColor}">
                <h2>{{ heading }}</h2>
                <input
                    v-model="inputValue"
                    :placeholder="placeholder"
                    @keydown.enter="emit('save', inputValue)"
                    @keydown.escape="emit('cancel')"
                    autofocus
                />
                <div class="modal-actions">
                    <button class="modal-cancel" @click="emit('cancel')">Cancel</button>
                    <button class="modal-save" @click="emit('save', inputValue)">Save</button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style scoped>

.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
}

.modal-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 32px;
    width: 100%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    border: 0.5px solid var(--border);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

h2 {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
}

input {
    padding: 10px 14px;
    border: 0.5px solid var(--border);
    border-radius: 8px;
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
}

input:focus {
    border-color: var(--accent-green);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--modal-accent) 35%, transparent);
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

.modal-cancel {
    background: transparent;  
    border: 0.5px solid var(--border);
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: border-color 0.2s;
}

.modal-cancel:hover {
    border-color: var(--text-secondary);
}

.modal-save {
    background: var(--accent-green);
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: white;
    cursor: pointer;
    transition: background-color 0.2s;
}

.modal-save:hover {
    background: var(--accent-green-hover);
}

.modal-enter-active {
    animation: overlayFadeIn 0.25s ease forwards;
}

.modal-leave-active {
    animation: overlayFadeOut 0.2s ease forwards;
}

.modal-enter-active .modal-card {
    animation: modalAppear 0.3s ease forwards;
}

.modal-leave-active .modal-card {
    animation: modalSink 0.2s ease forwards;
}

@keyframes overlayFadeOut {
    from { background: rgba(0,0,0,0.3); }
    to { background: rgba(0,0,0,0); }
}

@keyframes modalSink {
    from { opacity: 1; transform: scale(1) translateY(0); }
    to { opacity: 0; transform: scale(0.97) translateY(-8px); }
}

@keyframes overlayFadeIn {
    from {background: rgba(0,0,0,0)}
    to { background: rgba(0,0,0,0.3)}
}

@keyframes modalAppear {
    from { opacity: 0; transform: scale(0.97) translateY(-8px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}

</style>