import streamlit as st
from datetime import date, datetime, timedelta # Updated imports for date/time handling
from typing import Dict, Any, List, Optional
import json 

# --- 1. Workout Data Structure (Unchanged) ---

WORKOUT_DATA: Dict[str, Any] = {
    'warmup': {
        'title': "Warmup",
        'icon': "🕰️",
        'options': {
            # Warmup always uses option A in the combined routine
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

# Define the sequence of modules for a full workout session
MODULE_SEQUENCE = ['warmup', 'plyometrics', 'lowerStrength', 'dynamicBalance', 'staticBalance', 'ankleStrength']


# --- 2. State Management Functions ---

def init_state():
    """Initializes or resets the session state variables."""
    if 'view' not in st.session_state:
        st.session_state.view = 'schedule' # Default view is now 'schedule'
    if 'current_workout_type' not in st.session_state:
        st.session_state.current_workout_type = None # 'A' or 'B'
    if 'current_module_index' not in st.session_state:
        st.session_state.current_module_index = 0
    if 'current_exercise_index' not in st.session_state:
        st.session_state.current_exercise_index = 0
    if 'current_set' not in st.session_state:
        st.session_state.current_set = 1
    if 'workout_log' not in st.session_state:
        # Log stores completed sessions: [{'date': 'YYYY-MM-DD', 'type': 'A', 'time': 'HH:MM:SS'}, ...]
        st.session_state.workout_log = [] 
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = date.today()

def set_view(view: str):
    """Sets the current application view."""
    st.session_state.view = view

def start_workout(workout_type: str):
    """Initializes state for a new workout of type 'A' or 'B'."""
    st.session_state.current_workout_type = workout_type
    st.session_state.current_module_index = 0
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    set_view('workout')

def reset_app():
    """Resets all relevant state for a fresh start, returning to schedule view."""
    st.session_state.current_workout_type = None
    st.session_state.current_module_index = 0
    st.session_state.current_exercise_index = 0
    st.session_state.current_set = 1
    set_view('schedule')

def complete_set():
    """Logic for advancing sets and exercises in the full routine."""
    workout_type = st.session_state.current_workout_type
    current_mod_idx = st.session_state.current_module_index
    current_ex_idx = st.session_state.current_exercise_index
    current_mod_key = MODULE_SEQUENCE[current_mod_idx]
    
    # Determine which progression list to use (Option A or B)
    # Warmup always uses 'A', main modules use the selected workout_type ('A' or 'B')
    option_key = 'A' if current_mod_key == 'warmup' else workout_type
    
    progression = WORKOUT_DATA[current_mod_key]['options'][option_key]['progression']
    current_exercise = progression[current_ex_idx]

    # 1. Advance the set
    if st.session_state.current_set < current_exercise['sets']:
        st.session_state.current_set += 1
    
    # 2. Advance the exercise
    elif current_ex_idx < len(progression) - 1:
        st.session_state.current_exercise_index += 1
        st.session_state.current_set = 1
    
    # 3. Advance the module
    elif current_mod_idx < len(MODULE_SEQUENCE) - 1:
        st.session_state.current_module_index += 1
        st.session_state.current_exercise_index = 0
        st.session_state.current_set = 1
    
    # 4. Finish the entire workout
    else:
        log_workout_completion(workout_type)
        set_view('finished')

def log_workout_completion(workout_type: str):
    """Logs the completed workout to the session state log."""
    log_entry = {
        'date': st.session_state.selected_date.isoformat(),
        'time': datetime.now().strftime("%H:%M:%S"),
        'type': workout_type, # 'A' or 'B'
    }
    st.session_state.workout_log.append(log_entry)


# --- 3. Scheduling and Enforcement Logic ---

def get_schedule_info(selected_date: date) -> Dict[str, Any]:
    """
    Determines if a workout is allowed on the selected date and which type (A or B) is required.
    Enforces 3x/week and alternating A/B rules.
    """
    # Get the week number and year to check frequency
    # .isocalendar() returns (year, week_number, weekday)
    current_year, current_week, _ = selected_date.isocalendar()
    
    # Find all completed workouts within the current week
    weekly_logs = [
        log for log in st.session_state.workout_log
        if datetime.fromisoformat(log['date']).date().isocalendar()[:2] == (current_year, current_week)
    ]
    
    # Rule 1: Max 3 times per week
    if len(weekly_logs) >= 3:
        return {
            'allowed': False,
            'message': f"You have already completed 3 workouts this week (Week {current_week}). Rest is required!",
            'type': None
        }

    # Find the most recent completed workout ever, regardless of week
    recent_logs = sorted(st.session_state.workout_log, key=lambda x: datetime.strptime(x['date'] + x['time'], '%Y-%m-%d%H:%M:%S'), reverse=True)
    
    last_completed_type = None
    if recent_logs:
        last_completed_type = recent_logs[0]['type']
    
    # Determine the required workout type for alternating schedule
    if last_completed_type == 'A':
        required_type = 'B'
    elif last_completed_type == 'B':
        required_type = 'A'
    else:
        # If no previous logs, default to Workout A
        required_type = 'A'

    # Check if a workout is already logged for the selected date
    for log in weekly_logs:
        if log['date'] == selected_date.isoformat():
            return {
                'allowed': False,
                'message': f"Workout **{log['type']}** already logged for this date.",
                'type': None
            }
            
    # Rule 2: Alternating rule is satisfied, and frequency is good.
    return {
        'allowed': True,
        'message': f"Your next scheduled workout is **Workout {required_type}**.",
        'type': required_type
    }


# --- 4. View Functions ---

def display_schedule_view():
    """Displays the main screen with schedule enforcement."""
    st.title("🗓️ Ankle Fitness Scheduler")
    st.markdown(f"Today's date is **{date.today().strftime('%A, %b %d, %Y')}**.")
    st.markdown("Use the sidebar calendar to select the date you wish to log or start a workout.")
    
    schedule_info = get_schedule_info(st.session_state.selected_date)
    required_type = schedule_info['type']
    
    st.markdown("---")
    
    if schedule_info['allowed']:
        st.success(f"**SCHEDULED:** {schedule_info['message']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.header(f"Routine {required_type}")
            st.markdown(f"**{WORKOUT_DATA['plyometrics']['options'][required_type]['title']}**")
            st.markdown(f"**{WORKOUT_DATA['lowerStrength']['options'][required_type]['title']}**")
            st.markdown(f"**{WORKOUT_DATA['dynamicBalance']['options'][required_type]['title']}**")
            st.markdown(f"**{WORKOUT_DATA['staticBalance']['options'][required_type]['title']}**")
            st.markdown(f"**{WORKOUT_DATA['ankleStrength']['options'][required_type]['title']}**")

        with col2:
            st.markdown("### Start Workout")
            st.warning("This will start a full-session, alternating through all 6 modules.")
            st.button(
                f"Begin Workout {required_type}",
                key="btn_start_scheduled_workout",
                type="primary",
                use_container_width=True,
                on_click=start_workout,
                args=(required_type,)
            )

    else:
        st.error(f"**BLOCKED:** {schedule_info['message']}")
        st.warning("The app enforces a maximum of 3 workouts per week and strict A/B alternation.")


def display_workout_timer():
    """Displays the interactive workout step-tracker for the full routine."""
    workout_type = st.session_state.current_workout_type
    current_mod_idx = st.session_state.current_module_index
    current_ex_idx = st.session_state.current_exercise_index
    current_set = st.session_state.current_set

    if not workout_type or current_mod_idx >= len(MODULE_SEQUENCE):
        reset_app()
        return

    # Determine current module and its progression
    current_mod_key = MODULE_SEQUENCE[current_mod_idx]
    is_warmup = (current_mod_key == 'warmup')
    
    # Warmup always uses 'A', main modules use the session's workout_type
    option_key = 'A' if is_warmup else workout_type
    
    current_module = WORKOUT_DATA[current_mod_key]
    progression = current_module['options'][option_key]['progression']
    current_exercise = progression[current_ex_idx]
    
    max_sets = current_exercise['sets']
    unit_display = current_exercise.get('reps', current_exercise.get('time'))
    unit_label = current_exercise['unit']
    
    # --- Progress Calculation ---
    total_steps = 0
    completed_steps = 0
    
    # Calculate total steps by iterating through all modules and exercises
    for i, mod_key in enumerate(MODULE_SEQUENCE):
        opt = 'A' if mod_key == 'warmup' else workout_type
        mod_prog = WORKOUT_DATA[mod_key]['options'][opt]['progression']
        
        for ex in mod_prog:
            total_steps += ex['sets']
            
            if i < current_mod_idx:
                completed_steps += ex['sets']
            elif i == current_mod_idx:
                # Add completed sets for the current module
                if ex == current_exercise:
                    completed_steps += current_set - 1
                    break
                else:
                    completed_steps += ex['sets']

    progress_percentage = (completed_steps / total_steps) if total_steps > 0 else 0

    st.progress(progress_percentage, text=f"Total Session Progress: {int(progress_percentage * 100)}%")

    st.header(f"Session {workout_type}: {current_module['icon']} {current_module['title']}")
    st.subheader(f"Module {current_mod_idx + 1}/{len(MODULE_SEQUENCE)}")

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
            on_click=reset_app
        )
        st.caption("_Returns to schedule_")


def display_finished_view():
    """Displays the workout completion screen."""
    st.balloons()
    workout_type = st.session_state.current_workout_type
    st.title("🎉 Workout Complete!")
    st.subheader(f"You finished **Workout {workout_type}** for {st.session_state.selected_date.strftime('%A, %b %d')}.")
    
    st.success("Your workout has been logged! The next scheduled session will be the opposite type.")
    
    st.markdown("---")
    
    st.button(
        "Return to Schedule", 
        type="primary", 
        use_container_width=True, 
        on_click=reset_app
    )


# --- 5. Streamlit App Layout and Styling ---

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
        page_title="Ankle Fitness Scheduler",
        page_icon="🗓️",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    custom_styling()
    init_state()
    
    # --- Sidebar for Calendar and History ---
    with st.sidebar:
        st.header("🗓️ Schedule & Log")

        # Calendar Integration
        new_date = st.date_input("Select Workout Date", value=st.session_state.selected_date, key="date_picker")
        if new_date != st.session_state.selected_date:
            st.session_state.selected_date = new_date
            # Automatically reset view when date changes to start fresh for that day
            reset_app() 
            st.rerun()
        
        # Display frequency info for the current week
        current_year, current_week, _ = st.session_state.selected_date.isocalendar()
        weekly_logs = [
            log for log in st.session_state.workout_log
            if datetime.fromisoformat(log['date']).date().isocalendar()[:2] == (current_year, current_week)
        ]
        st.markdown(f"**Week {current_week} Progress:** {len(weekly_logs)}/3 Workouts Completed")
        
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
                st.caption(f"**{log['type']}** on {log_date} at {log['time']}")
        else:
            st.info("No workouts logged yet!")


    # --- Main Content Renderer ---
    if st.session_state.view == 'schedule':
        display_schedule_view()
    elif st.session_state.view == 'workout':
        display_workout_timer()
    elif st.session_state.view == 'finished':
        display_finished_view()

if __name__ == "__main__":
    main()