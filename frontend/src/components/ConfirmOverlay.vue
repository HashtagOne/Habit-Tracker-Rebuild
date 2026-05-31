<script setup>

const props = defineProps({
    visible: {
        type: Boolean,
        default: false
    },
    heading: {
        type: String,
        default: ""
    },
    message: {
        type: String,
        default: "This action cannot be undone."
    }
})

const emit = defineEmits(['confirm', 'cancel'])

</script>

<template>
    <Transition name="confirm-modal">
        <div class="confirm-overlay" v-if="visible" @click.self="emit('cancel')">
            <div class="confirm-card">
                <h2>{{ heading }}</h2>
                <p>{{ message }}</p>
                <div class="modal-actions">
                    <button class="confirm-cancel" @click="emit('cancel')">Cancel</button>
                    <button class="confirm-delete" @click="emit('confirm')">Delete</button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style scoped>
.confirm-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
}

.confirm-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 32px;
    width: 100%;
    max-width: 360px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    border: 0.5px solid var(--border);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

h2 {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
}

p {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 8px;
}

.confirm-cancel {
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

.confirm-cancel:hover {
    border-color: var(--text-secondary);
}

.confirm-delete {
    background: #9B4A2E;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: opacity 0.2s;
}

.confirm-delete:hover {
    opacity: 0.85;
}

.confirm-modal-enter-active {
    animation: overlayFadeIn 0.25s ease forwards;
}

.confirm-modal-leave-active {
    animation: overlayFadeOut 0.2s ease forwards;
}

.confirm-modal-enter-active .confirm-card {
    animation: modalAppear 0.3s ease forwards;
}

.confirm-modal-leave-active .confirm-card {
    animation: modalSink 0.3s ease forwards;
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
    from { background: rgba(0,0,0,0); }
    to { background: rgba(0,0,0,0.3); }
}

@keyframes modalAppear {
    from { opacity: 0; transform: scale(0.97) translateY(-8px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>