import streamlit as st
from datetime import date 
import datetime # Corrected: Added this crucial import
from typing import Dict, Any, List
import json 

# --- 1. Workout Data Structure ---

WORKOUT_DATA: Dict[str, Any] = {
    'warmup': {
        'title': "Warmup",
        'icon': "🕰️",
        'options': {
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
                    # FIX applied here: Changed 'detail' value from 'detail": "Short, quick jumps maintaining control.' to 'detail': "Short, quick jumps maintaining control."
                    {'name': "Double Leg Hops Forward/Backward", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Short, quick jumps maintaining control."}, 
                    {'name': "Double Leg Hops Side-to-Side", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Focus on controlled lateral movement."},
                    {'name': "Single Leg Hops In Place (Each Leg)", 'sets': 3, 'time': 30, 'unit': "s", 'detail': "Requires stability and power."},
                ],
            },
            'B': {
                'title': "Jumping Progression",
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
                'title': "Lateral Step Down",
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
                'title': "Reach with Feet",
                'description': "Challenge balance and hip mobility by reaching with the non-stance foot (Star Excursion).",
                'progression': [
                    {'name': "Reach with Feet (Each Leg)", 'sets': 3, 'time': 45, 'unit': "s", 'detail': "Reach with non-stance foot in various directions (forward, lateral, diagonal)."},
                ],
            },
            'B': {
                'title': "Reach with Hands",
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
                'title': "Eyes Closed Progression",
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
                'title': "Heel Raise Progression",
                'description': "Building calf strength and control through progressive overload (Option B: Heel Raise).",
                'progression': [
                    {'name': "Double Leg Heel Raise (Flat Ground)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Slow and controlled lift and descent."},
                    {'name': "Single Leg Heel Raise (Flat Ground)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Balance and control are key."},
                    {'name': "Single Leg Heel Raise (On Step)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Allows for full range of motion (deep stretch)."},
                    {'name': "Single Leg Heel Raise (On Step w/ Weight)", 'sets': 3, 'reps': 12, 'unit': "reps", 'detail': "Use a dumbbell for added resistance."},
                ],
            },
        },
    },
}

# --- 2. State Management Functions ---

def init_state():
    """Initializes or resets the session state variables."""
    if 'view' not in st.session_state:
        st.session_state.view = 'modules'
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
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

def select_module(key: str):
    """Handles module selection and transition to the options view."""
    st.session_state.selected_module = key
    st.session_state.selected_option = None
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    if key == 'warmup':
        # Warmup only has one option, go directly to workout
        st.session_state.selected_option = 'A'
        set_view('workout')
    else:
        set_view('options')

def select_option(key: str):
    """Handles option selection and transition to the workout timer view."""
    st.session_state.selected_option = key
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    set_view('workout')

def reset_app():
    """Resets all relevant state for a fresh start."""
    st.session_state.selected_module = None
    st.session_state.selected_option = None
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    set_view('modules')

def complete_set():
    """Logic for advancing sets and exercises."""
    module_key = st.session_state.selected_module
    option_key = st.session_state.selected_option
    progression = WORKOUT_DATA[module_key]['options'][option_key]['progression']
    current_idx = st.session_state.current_exercise_index
    current_exercise = progression[current_idx]
    
    if st.session_state.current_set < current_exercise['sets']:
        # Advance to the next set
        st.session_state.current_set += 1
    elif current_idx < len(progression) - 1:
        # Advance to the next exercise
        st.session_state.current_exercise_index += 1
        st.session_state.current_set = 1
    else:
        # Workout Finished
        log_workout_completion(module_key, option_key)
        set_view('finished')

def log_workout_completion(module_key: str, option_key: str):
    """Logs the completed workout to the session state log."""
    log_entry = {
        'date': st.session_state.selected_date.isoformat(),
        'time': datetime.datetime.now().strftime("%H:%M:%S"),
        'module': WORKOUT_DATA[module_key]['title'],
        'option': option_key,
        'full_key': module_key,
    }
    st.session_state.workout_log.append(log_entry)


# --- 3. View Functions ---

def display_modules_view():
    """Displays the main module selection screen."""
    st.title("💪 Ankle Fitness Flow")
    st.markdown("Select a **module** to begin your ankle fitness routine for **{date}**.".format(date=st.session_state.selected_date.strftime("%A, %b %d")))

    cols = st.columns(2)
    module_keys = list(WORKOUT_DATA.keys())

    for i, key in enumerate(module_keys):
        module = WORKOUT_DATA[key]
        with cols[i % 2]:
            # Custom styled card using markdown
            st.markdown(
                f"""
                <div class="module-card">
                    <h3>{module['icon']} {module['title']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Use a hidden button or form to trigger the state change reliably
            if st.button(f"Select {module['title']}", key=f"btn_select_{key}", use_container_width=True, help="Click to select this module."):
                select_module(key)

def display_options_view():
    """Displays the option (A or B) selection screen."""
    module_key = st.session_state.selected_module
    if not module_key:
        reset_app()
        return

    module = WORKOUT_DATA[module_key]
    st.title(f"Options for {module['icon']} {module['title']}")
    st.markdown("Choose the **progression** that fits your current needs.")

    st.button("← Back to Modules", on_click=reset_app)

    cols = st.columns(2)
    options = module['options']

    for i, (option_key, option) in enumerate(options.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(f"Option {option_key}: {option['title']}")
                st.markdown(f"*{option['description']}*")
                
                # Progression details
                st.markdown("**Progression Steps:**")
                progression_list = []
                for idx, exercise in enumerate(option['progression']):
                    unit_display = exercise.get('reps', exercise.get('time'))
                    unit_label = exercise['unit']
                    progression_list.append(f"**{idx + 1}.** {exercise['name']} ({exercise['sets']}x {unit_display} {unit_label})")
                
                st.markdown("\n".join(progression_list))

                st.button(
                    f"Start Option {option_key}", 
                    key=f"btn_start_option_{option_key}", 
                    use_container_width=True,
                    type="primary",
                    on_click=select_option, 
                    args=(option_key,)
                )

def display_workout_timer():
    """Displays the interactive workout step-tracker."""
    module_key = st.session_state.selected_module
    option_key = st.session_state.selected_option

    if not module_key or not option_key:
        reset_app()
        return

    progression = WORKOUT_DATA[module_key]['options'][option_key]['progression']
    current_idx = st.session_state.current_exercise_index
    current_set = st.session_state.current_set

    # Check if workout is ongoing
    if current_idx >= len(progression):
        # Should not happen if complete_set calls log_workout_completion correctly, but serves as a safeguard
        set_view('finished')
        return

    current_exercise = progression[current_idx]
    max_sets = current_exercise['sets']
    unit_display = current_exercise.get('reps', current_exercise.get('time'))
    unit_label = current_exercise['unit']
    
    # Progress Bar
    total_steps = sum(e['sets'] for e in progression)
    completed_steps = sum(e['sets'] for e in progression[:current_idx]) + current_set - 1
    progress_percentage = (completed_steps / total_steps)
    st.progress(progress_percentage, text=f"Overall Progress: {int(progress_percentage * 100)}%")

    st.header(f"{WORKOUT_DATA[module_key]['icon']} {WORKOUT_DATA[module_key]['title']}")

    # Current Exercise Display
    st.markdown(
        f"""
        <div class="workout-display">
            <p class="exercise-name">Exercise {current_idx + 1}/{len(progression)}</p>
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
            "✅ Set Complete", 
            key="btn_complete_set", 
            type="primary", 
            use_container_width=True,
            on_click=complete_set
        )

    with col_pause:
        st.button(
            "❌ End Workout Early", 
            key="btn_end_early", 
            use_container_width=True,
            on_click=reset_app
        )
        st.caption("_Returns to modules_")


def display_finished_view():
    """Displays the workout completion screen."""
    st.balloons()
    st.title("🎉 Workout Complete!")
    st.subheader(f"You finished your {WORKOUT_DATA[st.session_state.selected_module]['title']} routine for {st.session_state.selected_date.strftime('%A, %b %d')}.")
    
    st.success("Your workout has been logged! Check the 'Workout History' sidebar.")
    
    st.markdown("---")
    
    st.button(
        "Start New Module", 
        type="primary", 
        use_container_width=True, 
        on_click=reset_app
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
            
            /* Module Card Styling */
            .module-card {
                background-color: #374151; /* Card Background */
                padding: 1.25rem;
                border-radius: 0.75rem;
                margin-bottom: 1rem;
                border-left: 5px solid #2dd4bf;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .module-card h3 {
                margin-top: 0;
                margin-bottom: 0.5rem;
                color: #f9fafb;
                font-size: 1.25rem;
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

            /* Hide the redundant 'Select' buttons for card styling */
            [key^='btn_select_'] {
                visibility: hidden;
                height: 0;
                margin: 0;
                padding: 0;
            }

        </style>
    """, unsafe_allow_html=True)


def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Ankle Fitness App",
        page_icon="🦶",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    custom_styling()
    init_state()
    
    # --- Sidebar for Calendar and History ---
    with st.sidebar:
        st.header("🗓️ Calendar & Log")

        # Calendar Integration (using native st.date_input)
        new_date = st.date_input("Select Workout Date", value=st.session_state.selected_date, key="date_picker")
        if new_date != st.session_state.selected_date:
            st.session_state.selected_date = new_date
            # Automatically reset view when date changes to start fresh for that day
            reset_app() 
            st.rerun()

        st.markdown("---")
        st.subheader("Workout History")

        if st.session_state.workout_log:
            # Filter logs for the selected date
            selected_date_logs = [
                log for log in st.session_state.workout_log
                if log['date'] == st.session_state.selected_date.isoformat()
            ]

            if selected_date_logs:
                st.info(f"Workouts completed on **{st.session_state.selected_date.strftime('%b %d')}**:")
                for log in selected_date_logs:
                    st.caption(f"**{log['module']}** (Option {log['option']}) at {log['time']}")
            else:
                st.info(f"No workouts logged for {st.session_state.selected_date.strftime('%b %d')}.")
        else:
            st.info("No workouts logged yet!")

    # --- Main Content Renderer ---
    if st.session_state.view == 'modules':
        display_modules_view()
    elif st.session_state.view == 'options':
        display_options_view()
    elif st.session_state.view == 'workout':
        display_workout_timer()
    elif st.session_state.view == 'finished':
        display_finished_view()

if __name__ == "__main__":
    main()