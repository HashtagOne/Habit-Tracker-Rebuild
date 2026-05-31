<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)
const confirmPassword = ref("")

async function register() {
    error.value = ""
    loading.value = true

    try {

        if (password.value !== confirmPassword.value) {
            error.value = "Passwords do not match."
            loading.value = false
            return
        }

        const response = await fetch("http://localhost:5000/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json"}, 
            credentials: "include",
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        })

        const data = await response.json()

        if (!response.ok) {
            error.value = data.error
            return
        }

        router.push("/login")
    } catch (err) {
        error.value = "Something went wrong. Please try again."
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1>Hello, newcomer.</h1>
                <p> Register now to start writing down your habits.</p>
            </div>

            <div class="auth-fields">
                <div class="field">
                    <label>Username</label>
                    <input
                        v-model="username"
                        type="text"
                        placeholder="Your Username"
                        @keydown.enter="register"
                        autocomplete="off"
                    />
                </div>
                <div class="field">
                    <label>Password</label>
                    <input
                        v-model="password"
                        type="password"
                        placeholder="Your Password"
                        @keydown.enter="register"
                    />
                </div>
                <div class="field">
                    <label>Confirm Password</label>
                    <input
                        v-model="confirmPassword"
                        type="password"
                        placeholder="Confirm Your Password"
                        @keydown.enter="register"
                    />
                </div>
            </div>
            
            <p v-if="error" class="auth-error"> {{ error  }}</p>

            <button @click="register" :disabled="loading">
                {{  loading ? "Registering.." : "Register" }}
            </button>

            <p class="auth-switch">
                Already have an account?
                <RouterLink to="/login">Login Here </RouterLink>
            </p>
        </div>
    </div>
</template>

<style scoped>
    .auth-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--bg-primary);
        animation: fadeUp 0.8s ease both;
    }

    .auth-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 40px;
        width: 100%;
        max-width: 400px;
        display: flex;
        flex-direction: column;
        gap: 24px;
        border: 0.5px solid var(--border);
        box-shadow: 0 4px 24px var(--shadow);
    }

    .auth-header h1 {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }

    .auth-header p {
        color: var(--text-muted);
        font-size: 0.9rem;
    }

    .auth-fields {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .field {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05rem;
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
        box-shadow: 0 0 0 3px rgba(59,109,17,0.1);
    }

    button {
        background: var(--accent-green);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-family: "DM Sans", sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s, transform 0.1s;
        width: 100%;
    }

    button:hover {
        background-color: var(--accent-green-hover);
    }

    button:active {
        transform: scale(0.98);
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .auth-switch a {
       color: var(--accent-green);
       text-decoration: none; 
       font-weight: 600;
    }

    .auth-switch {
        text-align: center;
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    .auth-switch a:hover {
        text-decoration: none;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    a {
        position: relative;
        text-decoration: none;
    }

    a::after {
        content: '';
        position: absolute;
        bottom: 1.5px;
        left: 0;
        width: 0;
        height: 1.5px;
        background: var(--accent-green);
        transition: width 0.3s ease;
    }

    a:hover::after {
        width: 100%;
    }
</style>