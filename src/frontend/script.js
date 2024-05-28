/***************************************************************************************************************************
*** The implementation of the GUI is done through the 'eel' tool. All copyrights to this tool go to Chris Knott,
*** who is graciously distributing the project through the MIT License. 
*** The complete license can be found here: https://github.com/python-eel/Eel/blob/main/LICENSE
*** Special thanks to him and the team of contributors.
*** The public repository for 'eel' can be found here: https://github.com/python-eel/Eel
***************************************************************************************************************************/


/********************************************************************************************************
 * Handle the interactivity in the observations section
 ********************************************************************************************************/

const autonomous_container = document.getElementById("autonomous_container");
const teleop_container = document.getElementById("teleop_container");
const misc_container = document.getElementById("misc_container");

const aut_observations = [];
const teleop_observations = [];
const misc_observations = [];

function get_observations_array(counter){
    if(aut_observations.includes(counter)){
        return [autonomous_container, aut_observations];
    }else if(teleop_observations.includes(counter)){
        return [teleop_container, teleop_observations];
    }else if(misc_observations.includes(counter)){
        return [misc_container, misc_observations];
    }else{
        console.log("Observation not found in any array");
        return ["NA"];
    }

}

function move(arrow_id, up){
    const counter = arrow_id.substring(arrow_id.lastIndexOf("_") + 1);
    const response = get_observations_array(counter);
    if(response[0] === "NA"){
        return;
    }
    const observations_container = response[0];
    const observations = response[1];

    const index = observations.indexOf(counter);

    if(up){
        if(index === 0){
            return;
        }
        observations_container.insertBefore(document.getElementById("obs_" + counter), document.getElementById("obs_" + observations[index - 1]));
        observations.splice(index - 1, 0, observations.splice(index, 1)[0]); //move the array element up 1 spot
    }else{
        if(index === observations.length - 1){
            return;
        }
        observations_container.insertBefore(document.getElementById("obs_" + counter), document.getElementById("obs_" + observations[index + 1]).nextSibling);
        observations.splice(index + 1, 0, observations.splice(index, 1)[0]); //move the array element down 1 spot
    }

}

function move_up(e){
    e.preventDefault();
    const arrow_id = e.target.id;
    move(arrow_id, true);
}

function move_down(e){
    e.preventDefault();
    const arrow_id = e.target.id;
    move(arrow_id, false);
}

function erase_obs(e){
    e.preventDefault();
    const trash_id = e.target.id;
    const counter = trash_id.substring(trash_id.lastIndexOf("_") + 1);

    document.getElementById("obs_" + counter).remove();
    const response = get_observations_array(counter);
    const observations = response[1];
    const index = observations.indexOf(counter);
    observations.splice(index, 1);
}

function on_options_obs(e){
    const obs_type = e.target.value;
    const obs_id = e.target.id;
    const counter = obs_id.substring(obs_id.lastIndexOf("_") + 1);
    if(obs_type === "OPTIONS"){
        const obs_input = document.createElement("input");
        obs_input.type = "text";
        obs_input.className = "options_input";
        obs_input.id = "options_obs_" + counter;
        obs_input.placeholder = "Yes, No, Maybe, Other";
        obs_input.required = true;

        document.getElementById("obs_" + counter).appendChild(obs_input);

    } else if(document.getElementById("options_obs_" + counter)){
        document.getElementById("options_obs_" + counter).remove();
    }
}

function create_new_observation(str_counter, section){
    const observation = document.createElement("div");
    observation.className = "vert_obs_cont";
    observation.id = "obs_" + str_counter;

    const observation_template = `
    <div class="row observation">
        <label for="obs_label_${str_counter}" class="name_cell observation_label" contenteditable="true" role="textbox" id="label_${str_counter}"></label>:
        <select class="field_cell" name="obs_label_${str_counter}" id="obs_label_${str_counter}">
            <option value="EVERY_MATCH">Every Match</option>
            <option value="YES_OR_NO">Yes Or No</option>
            <option value="OPTIONS">Options</option>
            <option value="PARAGRAPH">Paragraph/Note</option>
        </select>
        <div class="control_buttons">
            <div class="arrow_container">
                <button type="button" class="arrows" id="up_${str_counter}">&#8593;</button>
                <button type="button" class="arrows" id="down_${str_counter}">&#8595;</button>
            </div>
            <button type="button" class="trash" id="trash_${str_counter}">&#x1F5D1;</button>
        </div>
    </div>
    `;
    
    observation.innerHTML = observation_template;

    switch (section){
        case "autonomous":
            autonomous_container.insertBefore(observation, autonomous_button);
            aut_observations.push(str_counter);
            break;
        case "teleop":
            teleop_container.insertBefore(observation, teleop_button);
            teleop_observations.push(str_counter);
            break;
        case "misc":
            misc_container.insertBefore(observation, misc_button);
            misc_observations.push(str_counter);
            break;
        default:
            console.log("Error 404. Button Not Found");
    }

    document.getElementById("obs_label_" + str_counter).addEventListener("change", on_options_obs);

    document.getElementById("trash_" + str_counter).addEventListener("click", erase_obs);
    document.getElementById("up_" + str_counter).addEventListener("click", move_up);
    document.getElementById("down_" + str_counter).addEventListener("click", move_down);
}


let obs_counter = 0;
const autonomous_button = document.getElementById("autonomous");
const teleop_button = document.getElementById("teleop");
const misc_button = document.getElementById("misc");

function add_observation(e){
    e.preventDefault();
    const button = e.target;

    const str_counter = obs_counter.toString();
    create_new_observation(str_counter, button.id);

    document.getElementById(`label_${str_counter}`).focus();
    
    obs_counter++;
}

autonomous_button.addEventListener("click", add_observation);
teleop_button.addEventListener("click", add_observation);
misc_button.addEventListener("click", add_observation);

/********************************************************************************************************
 * Sheets section
 ********************************************************************************************************/

const spreadsheet_url = document.getElementById("spreadsheet_url");
const language = document.getElementById("language");

const autonomous_subtitle = document.getElementById("autonomous_subtitle");
const teleop_subtitle = document.getElementById("teleop_subtitle");
const misc_subtitle = document.getElementById("misc_subtitle");

const check_teams = document.getElementById("sheet_check_teams");
const check_match_order = document.getElementById("sheet_check_match_order");
const check_scouting = document.getElementById("sheet_check_scouting");
const check_advanced_stats = document.getElementById("sheet_check_advanced_stats");
const check_ranking = document.getElementById("sheet_check_ranking");
const check_compare = document.getElementById("sheet_check_compare");

const name_teams = document.getElementById("sheet_name_teams");
const name_match_order = document.getElementById("sheet_name_match_order");
const name_advanced_stats = document.getElementById("sheet_name_advanced_stats");
const name_compare = document.getElementById("sheet_name_compare");


function translate_sheets(e){
    if(e.target.value === "en"){
        autonomous_subtitle.innerHTML = "AUTONOMOUS"; 
        teleop_subtitle.innerHTML = "TELEOPERATED"; 
        misc_subtitle.innerHTML = "MISCELLANEOUS";

        name_teams.value = "Teams";
        name_match_order.value = "Matches";
        name_advanced_stats.value = "Advanced Stats";
        name_compare.value = "Compare";
    }else{
        autonomous_subtitle.innerHTML = "AUTONOMO";
        teleop_subtitle.innerHTML = "TELEOPERADO";
        misc_subtitle.innerHTML = "MISCELANEO";

        name_teams.value = "Equipos";
        name_match_order.value = "Partidas";
        name_advanced_stats.value = "Estadisticas Avanzadas";
        name_compare.value = "Comparar";
    }
}

const submit_button = document.getElementById("submit_button");

function changed_spreadsheet_url(e){
    if(e.target.value){
        check_teams.disabled = false;
        check_match_order.disabled = false;
        check_advanced_stats.disabled = false;
        submit_button.innerHTML = "Edit Existing & Save";
    }else{
        check_teams.checked = true;
        check_teams.disabled = true;
        check_scouting.dispatchEvent(new Event("change"));
        check_ranking.dispatchEvent(new Event("change"));
        submit_button.innerHTML = "Create & Save";
    }
}

function changed_dependency_match_order(_e){
    if(spreadsheet_url.value) return;

    if(check_scouting.checked === true){
        check_match_order.checked = true;
        check_match_order.disabled = true;
    }else{
        check_match_order.disabled = false;
    }
}

function changed_dependency_advanced_stats(_e){
    if(spreadsheet_url.value) return;

    if(check_ranking.checked === true || check_compare.checked === true){
        check_advanced_stats.checked = true;
        check_advanced_stats.disabled = true;
    }else{
        check_advanced_stats.disabled = false;
    }
}

spreadsheet_url.addEventListener("change", changed_spreadsheet_url);
language.addEventListener("change", translate_sheets);

check_scouting.addEventListener("change", changed_dependency_match_order);
check_ranking.addEventListener("change", changed_dependency_advanced_stats);
check_compare.addEventListener("change", changed_dependency_advanced_stats);

/********************************************************************************************************
 * Load from save file
 ********************************************************************************************************/

const template_box = document.getElementById("template_box");
const template_en = document.getElementById("template_en");
const template_es = document.getElementById("template_es");
const no_template = document.getElementById("no_template");

function load_template(config){
    // load basic settings and credentials sections
    document.getElementById("tba_token").value = config["tba_token"];
    document.getElementById("team_code").value = config["team_code"];
    document.getElementById("team_name").value = config["team_name"];
    document.getElementById("event_name").value = config["event_name"];
    document.getElementById("year").value = config["year"];
    document.getElementById("event_key").value = config["event_key"];
    document.getElementById("spreadsheet_url").value = config["spreadsheet_url"];
    document.getElementById("language").value = config["language"];
    document.getElementById("timezone").value = config["timezone"];
    document.getElementById("num_matches").value = config["num_matches"];

    document.getElementById("spreadsheet_url").dispatchEvent(new Event("change"));
    document.getElementById("language").dispatchEvent(new Event("change"));

    // load observations section
    for(const section of Object.keys(config["observations"])){
        for(const obs of Object.keys(config["observations"][section])){
            if(obs === "__name__"){
                continue;
            }
            const str_counter = obs_counter.toString();
            let button;
            switch (section){
                case "autonomous":
                    button = autonomous_button;
                    break;
                case "teleop":
                    button = teleop_button;
                    break;
                case "misc":
                    button = misc_button;
                    break;
            }
            button.dispatchEvent(new Event("click"));
            document.getElementById("label_" + str_counter).innerHTML = obs;
            const new_obs_type = document.getElementById("obs_label_" + str_counter);
            new_obs_type.value = config["observations"][section][obs]["type"];
            new_obs_type.dispatchEvent(new Event("change"));
            if(new_obs_type.value === "OPTIONS"){
                document.getElementById("options_obs_" + str_counter).value = config["observations"][section][obs]["options"].join(", ");
            }
        }
    }

    // load sheets section
    for(const title of Object.keys(config["sheets"])){
        const check_mark = document.getElementById("sheet_check_" + title);
        if(!config["sheets"][title]["update"]){
            check_mark.checked = false;
        }
        check_mark.dispatchEvent(new Event("change"));
        document.getElementById("sheet_name_" + title).value = config["sheets"][title]["name"];
    }

    window.scrollTo(0, 0);

}

async function get_template(e){
    e.preventDefault();
    const button_id = e.target.id;
    switch (button_id){
        case "last_session":
            eel.get_JSON('config.json')(load_template);
            break;
        case "template_en":
            eel.get_JSON('examples/config_en.json')(load_template);
            break;
        case "template_es":
            eel.get_JSON('examples/config_es.json')(load_template);
            break;
    }
    template_box.remove();
}

template_en.addEventListener("click", get_template);
template_es.addEventListener("click", get_template);
no_template.addEventListener("click", get_template);

async function get_config(){
    let exists = await eel.config_exists()();
    if(exists){
        const button = document.createElement("button");
        button.type = "button";
        button.id = "last_session";
        button.innerHTML = "Load Last Session";
        button.style = "margin-right: 5px;";
        document.getElementById("template_buttons").insertBefore(button, template_en);
        button.addEventListener("click", get_template)
    }
}

get_config();


/********************************************************************************************************
 * Handle the submit process
 ********************************************************************************************************/


let spreadsheet_id;
function process_end(code){
    submit_button.disabled = false;
    if(code === 201 || code === 200){
        print_message("Done!")
        const url = `https://docs.google.com/spreadsheets/d/${spreadsheet_id}/edit`
        print_message(`You can find your spreadsheet <a href="${url}" target="_blank">here</a>, copying the link below, or you can look for it inside your Google Drive with the name 'Scouting${document.getElementById("team_name").value}${document.getElementById("event_name").value}${document.getElementById("year").value}'`);
        print_message(`Spreadsheet URL: ${url}`);
        if(code === 201){
            spreadsheet_url.value = url;
            spreadsheet_url.dispatchEvent(new Event("change"));
            print_message("The field 'Spreadsheet URL' above has been updated to reflect the newly created spreadsheet. Any new change will now update the created spreadsheet. If you wish to create a new one, leave the mentioned field empty.");

            // uncheck all checkboxes (except for advanced stats) after creating a spreadsheet for ease of editting later on.
            const form = document.form1.elements;
            for(let i = form.length - 15; i < form.length - 1; i += 2){
                const button_id = form[i].id
                const check_mark = document.getElementById(button_id);
                check_mark.checked = false;
                check_mark.dispatchEvent(new Event("change"));
            }
            document.getElementById("sheet_check_advanced_stats").checked = true;
        }
    }else if(code === 500){
        alert("Finished process with error. If the error is not clear from this console, open the dev console with F12 or try running the file src/main.py from a console.");
    }
}


function fill_obs_object(obs_arr, obs_name, dict){
    for(const counter of obs_arr){
        const label = document.getElementById("label_" + counter);
        const obs = document.getElementById("obs_label_" + counter);
        dict["observations"][obs_name][label.innerHTML] = {
            "type": obs.value,
        };

        // get the options from the textbox and convert them to an array
        if(obs.value === "OPTIONS"){
            const options_text = document.getElementById("options_obs_" + counter);
            const arr = options_text.value.split(",").map(function (value) {
                return value.trim();
             });
            dict["observations"][obs_name][label.innerHTML]["options"] = arr;
        }
    }
}

function get_config_JSON(){
    const dict = {};
    const form = document.form1.elements;

    // get the basic settings
    // there are 10 fields by default before the observations start. The number in the for should change if you add new fields in basic settings
    for(let i = 0; i < 10; i++){
        dict[form[i].id] = form[i].value;
    }

    //get the observations
    dict["observations"] = {
        "autonomous": {
            "__name__": autonomous_subtitle.innerHTML
        },
        "teleop": {
            "__name__": teleop_subtitle.innerHTML
        },
        "misc": {
            "__name__": misc_subtitle.innerHTML
        }
    };
    fill_obs_object(aut_observations, "autonomous", dict);
    fill_obs_object(teleop_observations, "teleop", dict);
    fill_obs_object(misc_observations, "misc", dict);


    // get the sheets
    // the initial number by which the length is substracted must increase by 2 for every new sheet added
    dict["sheets"] = {};
    for(let i = form.length - 16; i < form.length - 2; i += 2){
        const title = form[i].id.substring("sheet_check_".length);
        dict["sheets"][title] = {
            "name": form[i + 1].value,
            "update": form[i].checked
        };
    }

    return dict;
}

async function save_form(){
    reset_console();
    dict = get_config_JSON();
    await eel.submit_JSON(dict, false)();
    print_message("Saved!")
}

const save_button = document.getElementById("save_button");
save_button.addEventListener("click", save_form)

function handleSubmit(){
    dict = get_config_JSON();
    eel.submit_JSON(dict, true)(process_end);
    submit_button.disabled = true;
    return false;
}

console_display = document.getElementById("console_messages");

eel.expose(reset_console);
function reset_console(){
    console_display.innerHTML = "Output:";
}

eel.expose(print_error);
function print_error(message){
    console.log(message);
    message = message.replace(/>/g, "&gt;");
    message = message.replace(/</g, "&lt;");
    message = message.replace(/\n/g, "<br>");
    console_display.innerHTML += "<br> &gt; " + message;
    window.scrollTo(0, document.body.scrollHeight);
}

eel.expose(print_message);
function print_message(message){
    console.log(message);
    console_display.innerHTML += "<br> &gt; " + message;
    window.scrollTo(0, document.body.scrollHeight);
}

eel.expose(set_spreadsheet_id);
function set_spreadsheet_id(value){
    spreadsheet_id = value;
}