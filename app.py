import json
import streamlit as st
from groq import Groq

from tools import TOOLS


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_MODEL = "openai/gpt-oss-20b"


@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to Streamlit Secrets."
        )

    return Groq(api_key=api_key)


def groq_chat(messages, max_completion_tokens=500):
    client = get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
        max_completion_tokens=max_completion_tokens,
        include_reasoning=False
    )

    return response.choices[0].message.content.strip()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgentX",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# VIOLET / PURPLE THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(139, 92, 246, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(168, 85, 247, 0.10),
            transparent 25%
        ),
        #09070f;
    color: #f5f3ff;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* HEADER */

.agent-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 18px 24px;

    background: rgba(22, 16, 35, 0.92);

    border: 1px solid #39245a;
    border-radius: 16px;

    box-shadow:
        0 0 25px rgba(139, 92, 246, 0.08);

    margin-bottom: 32px;
}

.agent-name {
    color: #ffffff;
    font-size: 27px;
    font-weight: 750;
    letter-spacing: 1px;
}

.agent-name span {
    color: #a78bfa;
}

.agent-status {
    color: #34d399;
    font-size: 14px;
    font-weight: 600;
}


/* TITLE */

.workspace-title {
    color: #ffffff;
    font-size: 44px;
    font-weight: 750;
    letter-spacing: -1px;
}

.workspace-subtitle {
    color: #aaa1bd;
    font-size: 16px;
    margin-bottom: 28px;
}


/* CARDS */

.card {
    background:
        linear-gradient(
            145deg,
            rgba(30, 21, 47, 0.96),
            rgba(17, 12, 27, 0.96)
        );

    border: 1px solid #39245a;
    border-radius: 16px;

    padding: 23px;

    min-height: 235px;

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.22);
}

.card-title {
    color: #ddd6fe;
    font-size: 17px;
    font-weight: 650;
    letter-spacing: 0.5px;
    margin-bottom: 18px;
}


/* TOOLS */

.tool-item {
    color: #c8bfd6;
    padding: 10px 0;
    font-size: 15px;
}

.tool-check {
    color: #a78bfa;
    margin-right: 9px;
    font-weight: bold;
}


/* EXECUTION */

.execution-step {
    color: #aaa1bd;
    padding: 9px 0;
    font-size: 15px;
}


/* INPUT */

textarea {
    background-color: #110d19 !important;
    color: #f5f3ff !important;

    border: 1px solid #4c2f72 !important;
    border-radius: 12px !important;
}

textarea:focus {
    border-color: #8b5cf6 !important;

    box-shadow:
        0 0 0 1px #8b5cf6 !important;
}


/* BUTTON */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #9333ea
        );

    color: white;

    border: none;

    border-radius: 11px;

    padding: 12px 20px;

    font-size: 15px;
    font-weight: 650;

    transition: 0.2s;
}

.stButton > button:hover {
    background:
        linear-gradient(
            135deg,
            #8b5cf6,
            #a855f7
        );

    box-shadow:
        0 0 22px rgba(139, 92, 246, 0.35);
}


/* FILE */

[data-testid="stFileUploader"] {
    background-color: #110d19;
    border: 1px solid #39245a;
    border-radius: 13px;
    padding: 8px;
}

.file-info {
    color: #c4b5fd;

    background-color: #151020;

    border: 1px solid #49336b;

    border-radius: 10px;

    padding: 11px 15px;

    margin-top: 10px;
}


/* SECTION TITLES */

.results-title {
    color: #ffffff;

    font-size: 24px;

    font-weight: 700;

    margin-top: 35px;

    margin-bottom: 18px;
}


/* PLAN */

.plan-step {
    background:
        linear-gradient(
            135deg,
            #171021,
            #120d1a
        );

    border: 1px solid #49336b;

    border-left: 3px solid #8b5cf6;

    border-radius: 11px;

    padding: 14px;

    margin-top: 10px;

    color: #c8bfd6;
}


/* RESULT CARDS */

.result-card {
    background:
        linear-gradient(
            145deg,
            rgba(28, 20, 43, 0.98),
            rgba(15, 10, 23, 0.98)
        );

    border: 1px solid #3d285c;

    border-radius: 15px;

    padding: 20px;

    margin-bottom: 16px;

    box-shadow:
        0 7px 25px rgba(0, 0, 0, 0.20);
}

.result-card-title {
    color: #c4b5fd;

    font-size: 16px;

    font-weight: 700;

    letter-spacing: 0.6px;

    margin-bottom: 14px;
}

.result-main {
    color: #ffffff;

    font-size: 24px;

    font-weight: 700;
}

.result-label {
    color: #9187a3;

    font-size: 13px;

    margin-top: 7px;
}


/* METRICS */

.metric-box {
    background-color: #120d1b;

    border: 1px solid #38264f;

    border-radius: 10px;

    padding: 14px;

    text-align: center;
}

.metric-value {
    color: #c4b5fd;

    font-size: 24px;

    font-weight: 700;
}

.metric-label {
    color: #8f859e;

    font-size: 12px;

    margin-top: 4px;
}


/* MEMORY */

.memory-card {
    background:
        linear-gradient(
            145deg,
            rgba(32, 21, 50, 0.98),
            rgba(18, 12, 28, 0.98)
        );

    border: 1px solid #68459b;

    border-left: 4px solid #a78bfa;

    border-radius: 15px;

    padding: 20px;

    margin-bottom: 14px;

    box-shadow:
        0 0 25px rgba(139, 92, 246, 0.07);
}

.memory-step {
    color: #a78bfa;

    font-size: 13px;

    font-weight: 700;

    margin-bottom: 7px;
}

.memory-tool {
    color: #ffffff;

    font-size: 16px;

    font-weight: 650;
}

.memory-result {
    color: #c8bfd6;

    margin-top: 8px;

    line-height: 1.5;
}


/* FINAL RESPONSE */

.final-response {
    background:
        linear-gradient(
            145deg,
            rgba(39, 25, 61, 0.98),
            rgba(20, 13, 29, 0.98)
        );

    border: 1px solid #65439a;

    border-radius: 16px;

    padding: 23px;

    margin-top: 10px;

    box-shadow:
        0 0 30px rgba(139, 92, 246, 0.08);
}

.final-response-title {
    color: #ddd6fe;

    font-size: 18px;

    font-weight: 700;

    margin-bottom: 15px;
}


/* FOOTER */

.footer {
    border-top: 1px solid #2f2140;

    margin-top: 40px;

    padding-top: 18px;

    color: #756b82;

    text-align: center;

    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="agent-header">

    <div class="agent-name">
        🤖 AGENT<span>X</span>
    </div>

    <div class="agent-status">
        ● GROQ MODEL ONLINE
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="workspace-title">AUTONOMOUS AI AGENT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="workspace-subtitle">'
    'Give your agent a goal and watch it plan, select tools, '
    'execute actions, remember results, and respond.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TASK INPUT
# ============================================================

task = st.text_area(
    "Task",
    placeholder="Example: Calculate 25 * 48",
    height=130,
    label_visibility="collapsed"
)


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload a text file",
    type=["txt"]
)


if uploaded_file is not None:

    st.markdown(
        f"""
        <div class="file-info">
            📄 Uploaded:
            <b>{uploaded_file.name}</b>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# RUN BUTTON
# ============================================================

run_agent = st.button(
    "▶ RUN AGENT",
    use_container_width=True
)


st.write("")


# ============================================================
# MAIN DASHBOARD
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🧰 AVAILABLE TOOLS
        </div>

        <div class="tool-item">
            <span class="tool-check">✓</span>
            Calculator
        </div>

        <div class="tool-item">
            <span class="tool-check">✓</span>
            Text Analyzer
        </div>

        <div class="tool-item">
            <span class="tool-check">✓</span>
            File Analyzer
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    execution_box = st.empty()

    execution_box.markdown("""
    <div class="card">

        <div class="card-title">
            ⚡ AGENT EXECUTION
        </div>

        <div class="execution-step">
            ⚪ Understanding task
        </div>

        <div class="execution-step">
            ⚪ Creating plan
        </div>

        <div class="execution-step">
            ⚪ Executing tools
        </div>

        <div class="execution-step">
            ⚪ Generating result
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# EXECUTION STATUS
# ============================================================

def show_execution(
    understanding,
    planning,
    execution,
    result
):

    execution_box.markdown(
        f"""
        <div class="card">

            <div class="card-title">
                ⚡ AGENT EXECUTION
            </div>

            <div class="execution-step">
                {understanding} Understanding task
            </div>

            <div class="execution-step">
                {planning} Creating plan
            </div>

            <div class="execution-step">
                {execution} Executing tools
            </div>

            <div class="execution-step">
                {result} Generating result
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AGENT PLANNER
# ============================================================

def get_agent_decision(task):

    response = groq_chat(
        messages=[
            {
                "role": "system",
                "content": """
You are an AI planning agent.

Your job is to create a plan for completing
the user's task.

Available tools:

calculator
Use for mathematical calculations.

text_analyzer
Use for analyzing text.

file_analyzer
Use for analyzing an uploaded text file.

Return ONLY valid JSON.

The JSON must always have this structure:

{
    "steps": [
        {
            "tool": "calculator",
            "input": "25 * 48"
        }
    ]
}

For multiple actions:

{
    "steps": [
        {
            "tool": "calculator",
            "input": "25 * 48"
        },
        {
            "tool": "text_analyzer",
            "input": "AI agents can use tools."
        }
    ]
}

If no tool is required:

{
    "steps": []
}

Rules:

1. Return JSON only.
2. Do not use Markdown.
3. Do not add explanations.
4. Use only the available tools.
5. Each step must contain exactly one tool.
6. Keep each step independent.
"""
            },
            {
                "role": "user",
                "content": task
            }
        ]
    )

    return response


# ============================================================
# PARSE PLAN
# ============================================================

def parse_decision(decision_text):

    try:

        cleaned = decision_text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "", 1).replace("```", "", 1).strip()

        decision = json.loads(
            cleaned
        )

        steps = decision.get(
            "steps",
            []
        )

        if not isinstance(
            steps,
            list
        ):

            return []

        return steps

    except json.JSONDecodeError:

        return []


# ============================================================
# FINAL RESPONSE
# ============================================================

def generate_final_response(
    task,
    memory
):

    prompt = f"""
You are AgentX, an AI agent.

User request:
{task}

Agent execution memory:
{json.dumps(memory, indent=2)}

Use the execution memory to create the final answer.

IMPORTANT:

If multiple tools were used,
present the results as separate numbered points.

Example:

1. Calculator Result
   - Calculation: 25 × 48
   - Answer: 1200

2. Text Analysis
   - Words: 8
   - Characters: 43
   - Sentences: 2

If there is only one result,
give a concise structured answer.

Rules:

1. Use only actual information from the execution memory.
2. Do not invent information.
3. Do not mention JSON.
4. Do not mention internal implementation.
5. Do not mention internal tool execution.
6. Keep the answer concise.
7. Clearly separate different tool results.
"""

    response = groq_chat(
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    return response


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(
    tool_name,
    tool_input,
    uploaded_file
):

    if tool_name == "file_analyzer":

        if uploaded_file is None:

            return {
                "error": "No file uploaded."
            }

        try:

            file_text = uploaded_file.getvalue().decode(
                "utf-8"
            )

            tool_input = file_text

        except UnicodeDecodeError:

            return {
                "error": "File must be UTF-8 encoded."
            }


    if tool_name not in TOOLS:

        return {
            "error": f"Unknown tool: {tool_name}"
        }


    try:

        tool_function = TOOLS[tool_name]

        result = tool_function(
            tool_input
        )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# CALCULATOR RESULT CARD
# ============================================================

def show_calculator_result(
    tool_input,
    result
):

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-card-title">
                🔢 CALCULATOR RESULT
            </div>

            <div class="result-label">
                Calculation
            </div>

            <div style="color:#ddd6fe; margin-top:4px;">
                {tool_input}
            </div>

            <div class="result-label">
                Result
            </div>

            <div class="result-main">
                {result}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TEXT ANALYZER RESULT
# ============================================================

def show_text_result(result):

    if not isinstance(
        result,
        dict
    ):

        return

    words = result.get(
        "word_count",
        0
    )

    characters = result.get(
        "character_count",
        0
    )

    sentences = result.get(
        "sentence_count",
        0
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="metric-box">

                <div class="metric-value">
                    {words}
                </div>

                <div class="metric-label">
                    WORDS
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="metric-box">

                <div class="metric-value">
                    {characters}
                </div>

                <div class="metric-label">
                    CHARACTERS
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="metric-box">

                <div class="metric-value">
                    {sentences}
                </div>

                <div class="metric-label">
                    SENTENCES
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FILE ANALYZER RESULT
# ============================================================

def show_file_result(result):

    if not isinstance(
        result,
        dict
    ):

        return

    words = result.get(
        "word_count",
        0
    )

    characters = result.get(
        "character_count",
        0
    )

    lines = result.get(
        "line_count",
        0
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="metric-box">

                <div class="metric-value">
                    {words}
                </div>

                <div class="metric-label">
                    WORDS
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="metric-box">

                <div class="metric-value">
                    {characters}
                </div>

                <div class="metric-label">
                    CHARACTERS
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="metric-box">

                <div class="metric-value">
                    {lines}
                </div>

                <div class="metric-label">
                    LINES
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MEMORY CARD
# ============================================================

def show_memory(memory):

    if not memory:

        return


    st.markdown(
        '<div class="results-title">🧠 AGENT MEMORY</div>',
        unsafe_allow_html=True
    )


    for item in memory:

        step_number = item.get(
            "step",
            ""
        )

        tool_name = item.get(
            "tool",
            "unknown"
        )

        result = item.get(
            "result",
            ""
        )


        if isinstance(
            result,
            dict
        ):

            result_text = json.dumps(
                result,
                indent=2
            )

        else:

            result_text = str(
                result
            )


        st.markdown(
            f"""
            <div class="memory-card">

                <div class="memory-step">
                    MEMORY STEP {step_number}
                </div>

                <div class="memory-tool">
                    🔧 {tool_name}
                </div>

                <div class="memory-result">
                    {result_text.replace(chr(10), "<br>")}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RUN AGENT
# ============================================================

if run_agent:

    if not task.strip():

        st.warning(
            "Please enter a task first."
        )

    else:

        try:

            # =================================================
            # STEP 1 — UNDERSTANDING
            # =================================================

            show_execution(
                "🟡",
                "⚪",
                "⚪",
                "⚪"
            )


            with st.spinner(
                "Understanding task..."
            ):

                decision_text = get_agent_decision(
                    task
                )


            # =================================================
            # STEP 2 — PLANNING
            # =================================================

            show_execution(
                "🟢",
                "🟡",
                "⚪",
                "⚪"
            )


            steps = parse_decision(
                decision_text
            )


            if not steps:

                st.error(
                    "Agent could not create a valid plan."
                )

                with st.expander(
                    "Agent Raw Response"
                ):

                    st.code(
                        decision_text
                    )

                st.stop()


            # =================================================
            # AGENT PLAN
            # =================================================

            st.markdown(
                '<div class="results-title">'
                '🧠 AGENT PLAN'
                '</div>',
                unsafe_allow_html=True
            )


            for index, step in enumerate(
                steps,
                start=1
            ):

                tool = step.get(
                    "tool",
                    "unknown"
                )

                tool_input = step.get(
                    "input",
                    ""
                )


                st.markdown(
                    f"""
                    <div class="plan-step">

                        <b>STEP {index}</b>

                        <br><br>

                        🔧 Tool:
                        <b>{tool}</b>

                        <br>

                        📝 Input:
                        {tool_input}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # STEP 3 — EXECUTION
            # =================================================

            show_execution(
                "🟢",
                "🟢",
                "🟡",
                "⚪"
            )


            st.markdown(
                '<div class="results-title">'
                '⚡ TOOL RESULTS'
                '</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # AGENT MEMORY
            # =================================================

            memory = []


            # =================================================
            # EXECUTE EACH TOOL
            # =================================================

            for index, step in enumerate(
                steps,
                start=1
            ):

                tool_name = step.get(
                    "tool"
                )

                tool_input = step.get(
                    "input",
                    ""
                )


                if not tool_name:

                    continue


                with st.spinner(
                    f"Executing {tool_name}..."
                ):

                    result = execute_tool(
                        tool_name,
                        tool_input,
                        uploaded_file
                    )


                # =============================================
                # SAVE RESULT TO MEMORY
                # =============================================

                memory_item = {
                    "step": index,
                    "tool": tool_name,
                    "input": tool_input,
                    "result": result
                }


                memory.append(
                    memory_item
                )


                # =============================================
                # CALCULATOR
                # =============================================

                if tool_name == "calculator":

                    show_calculator_result(
                        tool_input,
                        result
                    )


                # =============================================
                # TEXT ANALYZER
                # =============================================

                elif tool_name == "text_analyzer":

                    st.markdown(
                        """
                        <div class="result-card">

                            <div class="result-card-title">
                                📝 TEXT ANALYZER
                            </div>
                        """,
                        unsafe_allow_html=True
                    )


                    show_text_result(
                        result
                    )


                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


                # =============================================
                # FILE ANALYZER
                # =============================================

                elif tool_name == "file_analyzer":

                    st.markdown(
                        """
                        <div class="result-card">

                            <div class="result-card-title">
                                📄 FILE ANALYZER
                            </div>
                        """,
                        unsafe_allow_html=True
                    )


                    show_file_result(
                        result
                    )


                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


            # =================================================
            # DISPLAY MEMORY
            # =================================================

            show_memory(
                memory
            )


            # =================================================
            # FINAL RESPONSE
            # =================================================

            show_execution(
                "🟢",
                "🟢",
                "🟢",
                "🟡"
            )


            with st.spinner(
                "Generating final response..."
            ):

                answer = generate_final_response(
                    task,
                    memory
                )


            show_execution(
                "🟢",
                "🟢",
                "🟢",
                "🟢"
            )


            st.markdown(
                '<div class="results-title">'
                '🤖 FINAL AGENT RESPONSE'
                '</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                """
                <div class="final-response">

                    <div class="final-response-title">
                        🤖 AgentX
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.write(
                answer
            )


        except Exception as e:

            st.error(
                f"Agent error: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

MODEL: GPT-OSS-20B
&nbsp;&nbsp;•&nbsp;&nbsp;

CLOUD: ✓
&nbsp;&nbsp;•&nbsp;&nbsp;

TOOLS: 3
&nbsp;&nbsp;•&nbsp;&nbsp;

MULTI-STEP AGENT: ✓
&nbsp;&nbsp;•&nbsp;&nbsp;

MEMORY: ✓

</div>
""", unsafe_allow_html=True)