import streamlit as st
from datetime import date, datetime
from typing import Dict, Any, List, Optional

# --- 1. Workout Data Structure (Unchanged) ---

WORKOUT_DATA: Dict[str, Any] = {
    'warmup': {
        'title': "Warmup",
        'icon': "🕰️",
        'options': {
            # Warmup is standardized as Option A
            'A': {
                'title': "Standard Warmup",
                'description': "Prepare your ankles with gentle movement.",
                'progression': [
                    {'name': "Ankle Circles (Each Direction)", 'sets': 2, 'time': 30, 'unit': "s", 'detail': "Slow, controlled circles to mobilize the joint."},
                    {'name': "Toe Taps (Alternating)", 'sets': 2, 'time': 60, 'unit': "s", 'detail': "Lift toes up and down rapidly to activate shin muscles."},
                ],
            },
        },
    },
    'plyometrics': {
        'title': "Plyometrics",
        'icon': "⚡",
        'options': {
            'A': {
                'title': "Hopping Progression",
                'description': "Hopping: Focus on quick ground contact and elastic energy.",
                'progression': [
                    {'name': "Double Leg Hops In Place", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Soft landing, minimal knee bend."},
                    {'name': "Double Leg Hops Forward/Backward", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Short, quick jumps maintaining control."},
                    {'name': "Double Leg Hops Side-to-Side", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Focus on controlled lateral movement."},
                    {'name': "Single Leg Hops In Place (Each Leg)", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Requires stability and power."},
                ],
            },
            'B': {
                'title': "Jumping Progression (Higher Intensity)",
                'description': "Jumping: Focus on maximal vertical and horizontal power.",
                'progression': [
                    {'name': "Vertical Jump", 'sets': 3, 'reps': 8, 'unit': "reps", 'detail': "Explode up, land soft."},
                    {'name': "Vertical Jump (2-to-1 Leg Landing)", 'sets': 3, 'reps': 8, 'unit': "reps", 'detail': "Jump on two feet, land and stabilize on one."},
                    {'name': "Single Leg Jumps In Place (Each Leg)", 'sets': 3, 'reps': 6, 'unit': "reps", 'detail': "Controlled landing for maximum stability."},
                    {'name': "Single Leg Jumps (Forward/Lateral/Diagonal)", 'sets': 3, 'reps': 6, 'unit': "reps", 'detail': "Focus on directional control and quickness."},
                ],
            },
        },
    },
    'lowerStrength': {
        'title': "Lower Extremity Strength",
        'icon': "💪",
        'options': {
            'A': {
                'title': "Single Leg RDL",
                'description': "Build hip and hamstring strength while challenging ankle stability.",
                'progression': [
                    {'name': "Single Leg RDL (Each Leg)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Keep back flat, extend trailing leg, focus on balance."},
                ],
            },
            'B': {
                'title': "Lateral Step Down (Higher Challenge)",
                'description': "Focus on eccentric control of the quad and ankle stabilizers, increase height.",
                'progression': [
                    {'name': "Lateral Step Down (Each Leg)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Control the movement down, increasing step height as you progress."},
                ],
            },
        },
    },
    'dynamicBalance': {
        'title': "Dynamic Balance",
        'icon': "🚶",
        'options': {
            'A': {
                'title': "Reach with Feet (Fundamental)",
                'description': "Challenge balance and hip mobility by reaching with the non-stance foot (Star Excursion).",
                'progression': [
                    {'name': "Reach with Feet (Each Leg)", 'sets': 3, 'time': 45, 'unit': "s", 'detail': "Reach with non-stance foot in various directions (forward, lateral, diagonal)."},
                ],
            },
            'B': {
                'title': "Reach with Hands (Perturbation)",
                'description': "Use an external object (like a light ball) to create dynamic perturbation.",
                'progression': [
                    {'name': "Reach with Hands (Each Leg)", 'sets': 3, 'time': 45, 'unit': "s", 'detail': "Maintain single-leg stance while reaching and controlling an object."},
                ],
            },
        },
    },
    'staticBalance': {
        'title': "Static Balance",
        'icon': "🧘",
        'options': {
            'A': {
                'title': "Eyes Open Progression",
                'description': "Relying on visual and somatosensory input.",
                'progression': [
                    {'name': "Arms Across Chest, Hard Ground (Each Leg)", 'sets': 3, 'time': 60, 'unit': "s", 'detail': "Avoid touching down, excessive trunk motion, or bracing non-stance limb. (Errors to avoid)"},
                    {'name': "Arms Across Chest, Foam Pad (Each Leg)", 'sets': 3, 'time': 60, 'unit': "s", 'detail': "Same stance, increased difficulty due to foam pad."},
                    {'name': "Kettlebell Pass, Foam Pad (Each Leg)", 'sets': 3, 'time': 60, 'unit': "s", 'detail': "Single leg stance while passing a light kettlebell side-to-side."},
                ],
            },
            'B': {
                'title': "Eyes Closed Progression (Advanced)",
                'description': "Highest level of challenge, relying entirely on somatosensory input.",
                'progression': [
                    {'name': "Eyes Closed, Hard Ground (Each Leg)", 'sets': 3, 'time': 60, 'unit': "s", 'detail': "Touch down is a major error."},
                    {'name': "Eyes Closed, Foam Pad (Each Leg)", 'sets': 3, 'time': 60, 'unit': "s", 'detail': "Eyes closed on an unstable surface."},
                ],
            },
        },
    },
    'ankleStrength': {
        'title': "Ankle Specific Strength",
        'icon': "🦶",
        'options': {
            'A': {
                'title': "Banded Eversion & Dorsiflexion",
                'description': "Targeting key muscles responsible for ankle stability (Option A: Eversion & Dorsiflexion).",
                'progression': [
                    {'name': "Banded Eversion (Each Leg)", 'sets': 3, 'reps': 25, 'unit': "reps", 'detail': "Pull foot outwards against band resistance."},
                    {'name': "Banded/Weighted Dorsiflexion (Each Leg)", 'sets': 3, 'reps': 25, 'unit': "reps", 'detail': "Pull foot upwards (toe to sky) against resistance."},
                ],
            },
            'B': {
                'title': "Single Leg Heel Raise Progression",
                'description': "Building calf strength and control through progressive overload (Option B: Heel Raise).",
                'progression': [
                    {'name': "Single Leg Heel Raise (Flat Ground)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Balance and control are key."},
                    {'name': "Single Leg Heel Raise (On Step)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Allows for full range of motion (deep stretch)."},
                    {'name': "Single Leg Heel Raise (On Step w/ Weight)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Use a dumbbell for added resistance."},
                ],
            },
        },
    },
}

# The sequence for the full workout session
MAIN_MODULE_KEYS = ['plyometrics', 'lowerStrength', 'dynamicBalance', 'staticBalance', 'ankleStrength']
FULL_SEQUENCE_KEYS = ['warmup'] + MAIN_MODULE_KEYS


# --- 2. State Management Functions ---

def init_state():
    """Initializes or resets the session state variables."""
    if 'view' not in st.session_state:
        st.session_state.view = 'home' # Start at the home/onboarding view
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'user_number' not in st.session_state:
        st.session_state.user_number = ''
    if 'user_age' not in st.session_state:
        st.session_state.user_age = ''
        
    if 'selected_options_map' not in st.session_state:
        # Dictionary to store user's A/B choice for each module: {'plyometrics': 'A', 'lowerStrength': 'B', ...}
        st.session_state.selected_options_map = {'warmup': 'A'}
        for key in MAIN_MODULE_KEYS:
            st.session_state.selected_options_map[key] = 'A' # Default to Option A
            
    if 'current_module_index' not in st.session_state:
        st.session_state.current_module_index = 0
    if 'current_exercise_index' not in st.session_state:
        st.session_state.current_exercise_index = 0
    if 'current_set' not in st.session_state:
        st.session_state.current_set = 1
    if 'workout_log' not in st.session_state:
        st.session_state.workout_log = [] 
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = date.today()

def set_view(view: str):
    """Sets the current application view."""
    st.session_state.view = view

def start_workout():
    """Initializes state for the execution of the selected routine."""
    # Ensure options are set before starting
    for key in MAIN_MODULE_KEYS:
        if st.session_state.selected_options_map.get(key) is None:
            st.warning("Please select an option (A or B) for all modules before starting.")
            return

    st.session_state.current_module_index = 0
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    set_view('workout')

def reset_session_state():
    """Resets all relevant state for a fresh workout selection, returning to selection view."""
    st.session_state.current_module_index = 0
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    # Resetting selections for a new daily plan (but keeping user details)
    st.session_state.selected_options_map = {'warmup': 'A'} 
    for key in MAIN_MODULE_KEYS:
        st.session_state.selected_options_map[key] = 'A'
    set_view('selection')

def log_workout_completion():
    """Logs the completed workout to the session state log."""
    log_entry = {
        'date': st.session_state.selected_date.isoformat(),
        'time': datetime.now().strftime("%H:%M:%S"),
        'routine': st.session_state.selected_options_map.copy(), # Log the specific A/B choices made
        'user': st.session_state.user_name
    }
    st.session_state.workout_log.append(log_entry)

def get_progression(module_key: str) -> List[Dict[str, Any]]:
    """Retrieves the progression list based on the user's selected option for that module."""
    option_key = st.session_state.selected_options_map.get(module_key, 'A') # Default safety to 'A'
    return WORKOUT_DATA[module_key]['options'][option_key]['progression']


def complete_set():
    """Logic for advancing sets, exercises, and modules in the full custom routine."""
    current_mod_idx = st.session_state.current_module_index
    current_ex_idx = st.session_state.current_exercise_index
    current_mod_key = FULL_SEQUENCE_KEYS[current_mod_idx]
    
    progression = get_progression(current_mod_key)
    current_exercise = progression[current_ex_idx]

    # 1. Advance the set
    if st.session_state.current_set < current_exercise['sets']:
        st.session_state.current_set += 1
    
    # 2. Advance the exercise
    elif current_ex_idx < len(progression) - 1:
        st.session_state.current_exercise_index += 1
        st.session_state.current_set = 1
    
    # 3. Advance the module
    elif current_mod_idx < len(FULL_SEQUENCE_KEYS) - 1:
        st.session_state.current_module_index += 1
        st.session_state.current_exercise_index = 0
        st.session_state.current_set = 1
    
    # 4. Finish the entire workout
    else:
        log_workout_completion()
        set_view('finished')


# --- 3. View Functions ---

def display_home_view():
    """Displays the personalized onboarding and registration screen."""
    st.title("Welcome to Ankle Fitness Flow 🚀")
    st.markdown("Before we start, please tell us a little about yourself to personalize your experience.")
    
    with st.form("user_details_form"):
        st.subheader("Your Details")
        
        name = st.text_input("Full Name", value=st.session_state.user_name if st.session_state.user_name else "", key="input_name")
        number = st.text_input("Contact Number", value=st.session_state.user_number, key="input_number")
        age = st.text_input("Age", value=st.session_state.user_age, key="input_age")
        
        submitted = st.form_submit_button("Start Personalized Routine", type="primary", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("Please enter your name to proceed.")
            elif not number.isdigit() or len(number) < 10:
                st.error("Please enter a valid contact number.")
            elif not age.isdigit():
                st.error("Please enter a valid age.")
            else:
                st.session_state.user_name = name.split()[0] # Use first name for greeting
                st.session_state.user_number = number
                st.session_state.user_age = age
                set_view('selection')
                st.rerun()

def display_selection_view():
    """Displays the plan review and module option selection page."""
    
    user_name = st.session_state.user_name if st.session_state.user_name else "Guest"
    st.title(f"Hello, {user_name}! 👋")
    st.markdown(f"Today's Date: **{st.session_state.selected_date.strftime('%A, %b %d')}**")

    st.subheader("Plan Your Workout: Choose Your Difficulty")
    st.info("Select **Option A** (default) or **Option B** for each module below. Option B usually offers an advanced or different focus.")
    
    # Display Warmup first (it's fixed)
    st.markdown("---")
    warmup = WORKOUT_DATA['warmup']
    st.markdown(f"### {warmup['icon']} {warmup['title']} (Fixed)")
    st.caption("Standard mobilization is always included.")
    
    # Display Selection for Main Modules
    for key in MAIN_MODULE_KEYS:
        module = WORKOUT_DATA[key]
        st.markdown("---")
        st.markdown(f"### {module['icon']} {module['title']}")
        
        col_A, col_B = st.columns(2)
        
        with col_A:
            st.markdown(f"**Option A: {module['options']['A']['title']}**")
            st.caption(module['options']['A']['description'])
            
            # Use radio button for selection
            if st.radio(
                "Select Option A", 
                options=[True, False], 
                index=0 if st.session_state.selected_options_map.get(key) == 'A' else 1,
                key=f'radio_{key}_A', 
                label_visibility="collapsed"
            ):
                st.session_state.selected_options_map[key] = 'A'
                
        with col_B:
            st.markdown(f"**Option B: {module['options']['B']['title']}**")
            st.caption(module['options']['B']['description'])

            if st.radio(
                "Select Option B", 
                options=[True, False], 
                index=0 if st.session_state.selected_options_map.get(key) == 'B' else 1,
                key=f'radio_{key}_B', 
                label_visibility="collapsed"
            ):
                st.session_state.selected_options_map[key] = 'B'
    
    st.markdown("---")
    
    # Summary and Start Button
    st.subheader("Ready to Go?")
    st.success("Your plan is set. You will perform 6 total modules in sequence.")
    
    # Display final routine summary
    routine_summary = "Routine: Warmup (A) → " + " → ".join([f"{WORKOUT_DATA[k]['icon']} ({st.session_state.selected_options_map.get(k, 'A')})" for k in MAIN_MODULE_KEYS])
    st.markdown(f"**{routine_summary}**")
    
    st.button(
        "Start Full Routine",
        key="btn_start_full_routine",
        type="primary",
        use_container_width=True,
        on_click=start_workout
    )


def display_workout_timer():
    """Displays the interactive workout step-tracker for the full custom routine."""
    
    current_mod_idx = st.session_state.current_module_index
    current_ex_idx = st.session_state.current_exercise_index
    current_set = st.session_state.current_set

    if current_mod_idx >= len(FULL_SEQUENCE_KEYS):
        set_view('finished')
        return

    # Get current exercise details
    current_mod_key = FULL_SEQUENCE_KEYS[current_mod_idx]
    current_module = WORKOUT_DATA[current_mod_key]
    option_key = st.session_state.selected_options_map.get(current_mod_key, 'A')
    
    progression = get_progression(current_mod_key)
    current_exercise = progression[current_ex_idx]
    
    max_sets = current_exercise['sets']
    unit_display = current_exercise.get('reps', current_exercise.get('time'))
    unit_label = current_exercise['unit']
    
    # --- Progress Calculation ---
    total_steps = 0
    completed_steps = 0
    
    for i, mod_key in enumerate(FULL_SEQUENCE_KEYS):
        opt = st.session_state.selected_options_map.get(mod_key, 'A')
        mod_prog = WORKOUT_DATA[mod_key]['options'][opt]['progression']
        
        for ex in mod_prog:
            total_steps += ex['sets']
            
            if i < current_mod_idx:
                completed_steps += ex['sets']
            elif i == current_mod_idx:
                if ex == current_exercise:
                    completed_steps += current_set - 1
                    break
                else:
                    completed_steps += ex['sets']

    progress_percentage = (completed_steps / total_steps) if total_steps > 0 else 0

    st.progress(progress_percentage, text=f"Total Session Progress: {int(progress_percentage * 100)}%")

    st.header(f"Module {current_mod_idx + 1}/{len(FULL_SEQUENCE_KEYS)}: {current_module['icon']} {current_module['title']}")
    st.subheader(f"Option {option_key} selected")

    # Current Exercise Display
    st.markdown(
        f"""
        <div class="workout-display">
            <p class="exercise-name">Exercise {current_ex_idx + 1}/{len(progression)}</p>
            <h2>{current_exercise['name']}</h2>
            <div class="sets-reps-box">
                <span class="set-counter">SET {current_set} / {max_sets}</span>
                <span class="reps-time">🎯 {unit_display} {unit_label}</span>
            </div>
            <p class="detail-text">{current_exercise['detail']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Controls
    col_pause, col_complete = st.columns([1, 4])
    
    with col_complete:
        st.button(
            "✅ Set Complete (Advance)", 
            key="btn_complete_set", 
            type="primary", 
            use_container_width=True,
            on_click=complete_set
        )

    with col_pause:
        st.button(
            "❌ End Session Early", 
            key="btn_end_early", 
            use_container_width=True,
            on_click=reset_session_state
        )
        st.caption("_Returns to planning_")


def display_finished_view():
    """Displays the workout completion screen."""
    st.balloons()
    user_name = st.session_state.user_name if st.session_state.user_name else "Champion"
    st.title(f"Great work, {user_name}! 🎉")
    st.subheader(f"You successfully completed your full customized routine for {st.session_state.selected_date.strftime('%A, %b %d')}.")
    
    st.success("Your session has been logged! Check the 'Workout History' sidebar.")
    
    st.markdown("---")
    
    st.button(
        "Plan Another Workout", 
        type="primary", 
        use_container_width=True, 
        on_click=reset_session_state
    )


# --- 4. Streamlit App Layout and Styling ---

def custom_styling():
    """Injects custom CSS for a modern, flowing dark UI/UX."""
    st.markdown("""
        <style>
            .stApp {
                background-color: #1f2937; /* Dark Gray Background */
                color: #f9fafb; /* Light Text */
                font-family: 'Inter', sans-serif;
            }
            /* Main Content Container */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 700px;
            }
            h1, h2, h3 {
                color: #2dd4bf; /* Teal Accent */
                font-weight: 800;
            }
            .stButton>button {
                border-radius: 0.5rem;
                transition: all 0.3s ease;
                font-weight: bold;
            }
            .stButton>button:hover {
                box-shadow: 0 4px 6px -1px rgba(45, 212, 191, 0.4), 0 2px 4px -2px rgba(45, 212, 191, 0.4);
            }
            
            /* Radio button adjustment for cleaner look */
            .stRadio > label {
                padding-top: 5px;
            }
            .stRadio div[role="radiogroup"] {
                flex-direction: row; /* Make A/B selection horizontal */
                gap: 15px;
                margin-top: 10px;
            }
            /* Styling for the hidden radio button label */
            .stRadio label[aria-label="Select Option A"], .stRadio label[aria-label="Select Option B"] {
                margin-top: 5px; 
            }
            
            /* Workout Display Styling */
            .workout-display {
                background-color: #111827;
                padding: 2rem;
                border-radius: 1rem;
                text-align: center;
                margin-bottom: 1.5rem;
                border: 2px solid #2dd4bf;
            }
            .exercise-name {
                color: #9ca3af;
                font-size: 1rem;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            }
            .workout-display h2 {
                color: #f9fafb;
                font-size: 2.25rem;
                margin-bottom: 1.5rem;
            }
            .sets-reps-box {
                display: flex;
                justify-content: center;
                gap: 2rem;
                font-weight: bold;
            }
            .set-counter {
                color: #2dd4bf;
                font-size: 1.5rem;
            }
            .reps-time {
                color: #f9fafb;
                font-size: 1.5rem;
            }
            .detail-text {
                color: #9ca3af;
                font-style: italic;
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Personalized Ankle Fitness",
        page_icon="🦶",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    custom_styling()
    init_state()
    
    # --- Sidebar for Calendar and History ---
    with st.sidebar:
        user_name = st.session_state.user_name if st.session_state.user_name else "User"
        st.header(f"Hello, {user_name}!")
        
        # Calendar Integration
        new_date = st.date_input("Select Workout Date", value=st.session_state.selected_date, key="date_picker")
        if new_date != st.session_state.selected_date:
            st.session_state.selected_date = new_date
            # Automatically reset view when date changes to start fresh for that day
            reset_session_state() 
            st.rerun()

        st.markdown("---")
        st.subheader("Workout History")
        
        if st.session_state.workout_log:
            # Sort all logs by date/time (most recent first)
            sorted_logs = sorted(
                st.session_state.workout_log, 
                key=lambda x: datetime.strptime(x['date'] + x['time'], '%Y-%m-%d%H:%M:%S'), 
                reverse=True
            )
            
            st.info(f"Last **{len(sorted_logs)}** logged sessions:")
            
            for log in sorted_logs:
                log_date = datetime.fromisoformat(log['date']).strftime('%b %d')
                
                # Show the combination of A/B choices made for the session
                choices = "/".join(log['routine'][k] for k in MAIN_MODULE_KEYS)
                
                st.caption(f"**Custom ({choices})** on {log_date} at {log['time']}")
        else:
            st.info("No workouts logged yet!")


    # --- Main Content Renderer ---
    if st.session_state.view == 'home':
        display_home_view()
    elif st.session_state.view == 'selection':
        display_selection_view()
    elif st.session_state.view == 'workout':
        display_workout_timer()
    elif st.session_state.view == 'finished':
        display_finished_view()

if __name__ == "__main__":
    main()