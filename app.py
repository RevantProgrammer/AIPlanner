import streamlit as st
from services.plannerService import PlannerApplicationService
from config.settings import get_settings
from time import sleep


@st.cache_resource
def get_cached_planner_llm():
    return PLANNER_SERVICE.get_planner()


@st.cache_data
def get_cached_constants():
    return get_settings()


@st.cache_resource
def get_cached_planner_service():
    return PlannerApplicationService(config=get_cached_constants())


def go_to_stage(stage):
    st.session_state.stage = stage
    st.rerun()


def reset_plan_state():
    st.session_state.curr_plan = None
    st.session_state.history = []
    st.session_state.finalised_plan_flag = False


def render_initial_stage():
    st.title("1. 📊 Event Planner AI")
    st.write("Click the button below to process new form submissions.")
    executor_button = st.button("Run Planner")
    if executor_button:
        go_to_stage("fetch_data")


def render_fetch_stage():
    st.title("2. Fetch Stage")

    if not st.session_state.fetch_done:
        with st.spinner("Fetching unplanned rows..."):
            try:
                num_rows, processed_rows = PLANNER_SERVICE.fetch_unplanned_rows()
            except Exception as e:
                st.error(f"Failed to fetch rows: {e}")
                return

        st.session_state.processed_rows = processed_rows
        st.session_state.num_rows = num_rows
        st.session_state.fetch_done = True

        if num_rows > 0:
            st.session_state.curr_row = processed_rows[st.session_state.current_queue_index]["data"]
            st.session_state.curr_row_idx = processed_rows[st.session_state.current_queue_index]["row_index"]

    if st.session_state.get("num_rows", 0) == 0:
        st.success("✅ No new rows to process. No planning is required! You can close this tool safely.")
        return

    st.success(f"✅ Found {st.session_state.num_rows} row(s) to process.")
    st.info(f"Selected Row {st.session_state.curr_row_idx} to start planning")
    st.json(st.session_state.curr_row)

    if st.button("Validate Data"):
        go_to_stage("validate")


def render_validate_page():
    st.title("3. Validation and Normalisation Stage")

    with st.spinner("Validating and Normalising data..."):
        try:
            st.session_state.curr_row = PLANNER_SERVICE.validate(st.session_state.curr_row)
        except Exception as e:
            st.error(f"Failed to validate data: {e}")
            st.json(st.session_state.curr_row)
            return

    st.subheader("Validated Data:")
    st.json(st.session_state.curr_row)
    planner_button = st.button("Generate Plan")
    if planner_button:
        go_to_stage("process")


def render_process_stage():
    st.title("4. Plan Stage")
    st.subheader(f"Processing Row {st.session_state.curr_row_idx}")

    # FEEDBACK LOOP

    if st.session_state.curr_plan is None:
        with st.spinner("Connecting to LLM..."):
            try:
                local_planner_llm = get_cached_planner_llm()
            except Exception as e:
                st.error(f"LLM connecftion failed, Error: {e}")
                return

        placeholder = st.empty()
        response = ""

        with st.status("Thinking...", expanded=True) as status:
            try:
                for partial in local_planner_llm.generate_plan(st.session_state.curr_row):
                    response = partial
                    placeholder.markdown(response)
                    status.update(label="Generating plan...", state="running")
            except Exception as e:
                st.error(f"LLM response failed, Error: {e}")
                return

            status.update(label="Done", state="complete")

        st.session_state.curr_plan = response
        st.session_state.history = []
        st.rerun()

    if st.session_state.curr_plan:
        if st.session_state.history:
            st.subheader("Feedback History")
            for i, fb in enumerate(st.session_state.history, 1):
                st.write(f"{i}. {fb}")

        if st.session_state.clear_feedback:
            st.session_state.feedback_input = ""
            st.session_state.clear_feedback = False

        st.text_area(
            "Refine or modify the plan:",
            key="feedback_input",
            placeholder="Enter feedback and press Update Plan..."
        )

        col1, col2, col3 = st.columns(3)

        if st.session_state.finalised_plan_flag:
            st.success("Final Plan Approved!")
            st.write("🚀 Onto the implementation layer!")
            st.balloons()
        spinner_placeholder = st.empty()
        placeholder = st.empty()

        with col1:
            if st.button("Update Plan", disabled=not st.session_state.feedback_input.strip()):
                updated_plan = ""

                with st.status("Reading feedback...", expanded=True) as status:
                    local_planner_llm = get_cached_planner_llm()
                    try:
                        for partial in local_planner_llm.refine_plan(
                                plan=st.session_state.curr_plan,
                                feedback=st.session_state.feedback_input
                        ):
                            updated_plan = partial
                            placeholder.markdown(updated_plan)
                            status.update(label="Refining plan...", state="running")
                    except Exception as e:
                        st.error(f"LLM response failed, Error: {e}")
                        return

                    status.update(label="Done", state="complete")

                st.session_state.curr_plan = updated_plan
                st.session_state.history.append(st.session_state.feedback_input)
                st.session_state.clear_feedback = True

                st.rerun()

        with col2:
            if st.button("Start Over"):
                reset_plan_state()
                st.rerun()

        with col3:
            if st.button("Satisfied ✅"):
                st.session_state.finalised_plan_flag = True
                st.rerun()

        st.subheader("Current Plan")
        st.markdown(st.session_state.curr_plan)

    if st.session_state.finalised_plan_flag:
        with spinner_placeholder:
            with st.spinner("Loading the next page"):
                sleep(2.5)
        go_to_stage("implement")


def render_implement_stage():
    st.title("5. Implementation Stage")
    print(st.session_state.curr_plan)
    if st.session_state.pdf_content is None:
        with st.spinner("Transforming the plan into a PDF..."):
            try:
                st.session_state.pdf_content = PLANNER_SERVICE.make_pdf(st.session_state.curr_plan)
            except Exception as e:
                st.error(f"Failed to generate PDF, Error: {e}")
                return
    st.success("Plan saved into a PDF!")
    st.download_button(
        label="Download Marketing Plan PDF",
        data=st.session_state.pdf_content,
        file_name="marketing_plan.pdf",
        mime="application/pdf"
    )
    finish_button = st.button("Finish Pipeline")
    if finish_button:
        go_to_stage("finish")


def render_finish_stage():
    st.title("Task Complete!")
    if not st.session_state.FINISH_PIPELINE:
        with st.spinner("Marking row as planned in database..."):
            try:
                PLANNER_SERVICE.mark_row_complete(st.session_state.curr_row_idx)
            except Exception as e:
                st.error(f"Failed to change 'Planned' column value in database: {e}")
                return
        st.session_state.FINISH_PIPELINE = True

    st.subheader("Final Remarks: We have gone through the whole pipeline and created the planner! Hope you "
                 "liked the services")

    if st.session_state.current_queue_index + 1 >= st.session_state.num_rows:
        st.info("Planner complete and row marked as planned in Google Sheets.")
        st.success("✅ All rows that were checked at the start have been planned! You can safely close this tool now!")
        return

    next_iteration_button = st.button("Process Next Row")
    if next_iteration_button:
        st.session_state.current_queue_index += 1
        st.session_state.stage = "validate"
        st.session_state.curr_row_idx = st.session_state.processed_rows[st.session_state.current_queue_index][
            "row_index"]
        st.session_state.curr_row = st.session_state.processed_rows[st.session_state.current_queue_index]["data"]
        reset_plan_state()
        st.session_state.pdf_content = None
        st.session_state.FINISH_PIPELINE = False
        st.rerun()


def run_pipeline():
    STAGES = {
        "initial": render_initial_stage,
        "fetch_data": render_fetch_stage,
        "validate": render_validate_page,
        "process": render_process_stage,
        "implement": render_implement_stage,
        "finish": render_finish_stage
    }

    STAGES[st.session_state.stage]()


def initialise_session_states():
    if "stage" not in st.session_state:
        st.session_state.stage = "initial"

    if "pdf_content" not in st.session_state:
        st.session_state.pdf_content = None

    if "current_queue_index" not in st.session_state:
        st.session_state.current_queue_index = 0

    if "fetch_done" not in st.session_state:
        st.session_state.fetch_done = False

    if "curr_plan" not in st.session_state:
        st.session_state.curr_plan = None

    if "feedback_input" not in st.session_state:
        st.session_state.feedback_input = ""

    if "clear_feedback" not in st.session_state:
        st.session_state.clear_feedback = False

    if "finalised_plan_flag" not in st.session_state:
        st.session_state.finalised_plan_flag = False

    if "FINISH_PIPELINE" not in st.session_state:
        st.session_state.FINISH_PIPELINE = False


if __name__ == "__main__":
    PLANNER_SERVICE = get_cached_planner_service()
    initialise_session_states()
    run_pipeline()
