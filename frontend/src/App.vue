<script setup>
import UniLogo from './assets/URT.png'
import { ref } from "vue"
import axios from "axios"
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const origin = ref("")
const destination = ref("")
const departure_date = ref("")

const results = ref(null)
const fictional = ref([])
const duffels = ref([])
const analysis = ref(null)

const bshowFlight = ref(false)
const selectedFlight = ref(null)
const status = ref("idle")

const temp_newSearch = ref("")

const showWhich = ref(false)
const text_showWhich = ref("IATA code direct input")

const userQuery = ref("")
function showFlight(flight) {
    
    selectedFlight.value = flight
    bshowFlight.value = true
}
async function searchFlights(){
    status.value = "pending"
    const response = await axios.post(
         `${API_BASE_URL}/api/flights/search/`,
        {
            origin: origin.value,
            destination: destination.value,
            departure_date: departure_date.value
        }
    )
    status.value = "success"
    results.value = response.data
    fictional.value = response.data.fictional
    duffels.value = response.data.duffels
    analysis.value = response.data.analysis
}
async function new_searchFlights() {

    status.value = "pending"

    try {

        const new_response = await axios.post(
            `${API_BASE_URL}/api/flights/search/new/`,
            {
                query: userQuery.value,
                departure_date: departure_date.value
            }
        )

        console.log("NEW SEARCH RESPONSE:")
        console.log(new_response.data)

        analysis.value = new_response.data.analysis

        status.value = "success"

    } catch (error) {

        console.error(
            "New flight search failed:",
            error
        )

        status.value = "error"
    }
}
async function changeShow() {
    showWhich.value = !showWhich.value
    if (showWhich.value){
        text_showWhich.value = "IATA code direct input"
    }
    else{
        text_showWhich.value = "AI dynamic search"
    }
}
</script>





    


<template>
<img :src="UniLogo" alt="UniLogo">
<h1>
Jamesonian Aerospace Travel
</h1>
<pre>

</pre>


<button @click="changeShow">
{{ text_showWhich }}
</button>
<div>
<input
    v-if = "showWhich"
    v-model="origin"
    placeholder="Origin"
/>


<input
    v-if = "showWhich"
    v-model="destination"
    placeholder="Destination"
/>

<textarea
    v-if="!showWhich"
    v-model="userQuery"
    class="travel_input"
    placeholder="Tell us where you want to go and your preferences..."
    rows="4"
></textarea>
</div>
<input
    type="date"
    v-model="departure_date"
/>
<button
v-if = "!showWhich"
@click="new_searchFlights">
    newSearch
</button>

<button 
v-if = "showWhich"
@click="searchFlights">
    Search
</button>

<div v-if="status === 'pending'">
    Searching flights...
</div>
<div v-if="status === 'success'">
    Search completed!
</div>

<div v-if="status === 'error'">
    Search failed. Check the browser console.
</div>
<el-table
    v-if="analysis"
    :data="analysis.flights_filtered"
    border
    stripe
    style="width: 100%"
>
    <el-table-column label="Flight" width="150">
        <template #default="scope">
            <el-button
                type="primary"
                link
                @click="showFlight(scope.row)"
            >
                {{ scope.row.airline.iata_code }}{{ scope.row.flight_number }}
            </el-button>
        </template>
    </el-table-column>

    <el-table-column
        prop="price_score"
        label="Price Score"
        width="120"
    />

    <el-table-column
        prop="layover_score"
        label="Layover Score"
        width="130"
    />

    <el-table-column
        prop="time_score"
        label="Time Score"
        width="110"
    />

    <el-table-column
        prop="final_score"
        label="Final Score"
        width="120"
    />

    <el-table-column
        prop="price"
        label="Price"
        width="130"
    >
        <template #default="scope">
            {{ scope.row.price }} {{ scope.row.currency }}
        </template>
    </el-table-column>

    <el-table-column
        label="Depature and Arrival"
        min-width="250"
    >
        <template #default="scope">
            {{ scope.row.segments[0].departure_airport.iata_code }}

        →

        {{ scope.row.segments[scope.row.segments.length - 1].arrival_airport.iata_code }}
        </template>
    </el-table-column>
</el-table>
<el-dialog
    v-model="bshowFlight"
    title="Flight Details"
    width="800px"
>
    <div v-if="selectedFlight">

        <!-- Flight title -->

        <h2>
            {{ selectedFlight.airline.iata_code }}
            {{ selectedFlight.flight_number }}
        </h2>


        <!-- ========================= -->
        <!-- Basic Information -->
        <!-- ========================= -->

        <h3>Basic Information</h3>

        <el-table
            :data="[selectedFlight]"
            border
            style="width: 100%"
        >

            <el-table-column
                prop="flight_number"
                label="Flight Number"
            />

            <el-table-column
                label="Price"
            >
                <template #default="scope">
                    {{ scope.row.currency }}
                    {{ scope.row.price }}
                </template>
            </el-table-column>

            <el-table-column
                label="Currency"
                prop="currency"
            />

            <el-table-column
                label="Flight ID"
                prop="id"
            />

        </el-table>


        <!-- ========================= -->
        <!-- Airline -->
        <!-- ========================= -->

        <h3>Airline</h3>

        <el-table
            :data="[selectedFlight.airline]"
            border
            style="width: 100%"
        >

            <el-table-column
                prop="iata_code"
                label="IATA"
            />

            <el-table-column
                prop="name"
                label="Airline"
            />

            <el-table-column
                prop="country"
                label="Country"
            />

            <el-table-column
                prop="rating"
                label="Rating"
            />

        </el-table>


        <!-- ========================= -->
        <!-- Aircraft -->
        <!-- ========================= -->

        <h3>Aircraft</h3>

        <el-table
            :data="[selectedFlight.aircraft]"
            border
            style="width: 100%"
        >

            <el-table-column
                prop="model"
                label="Model"
            />

            <el-table-column
                prop="manufacturer"
                label="Manufacturer"
            />

            <el-table-column
                prop="seats"
                label="Seats"
            />

        </el-table>


        <!-- ========================= -->
        <!-- Scores -->
        <!-- ========================= -->

        <h3>Analysis</h3>

        <el-table
            :data="[selectedFlight]"
            border
            style="width: 100%"
        >

            <el-table-column
                label="Price Score"
            >
                <template #default="scope">
                    {{ scope.row.price_score ?? "N/A" }}
                </template>
            </el-table-column>

            <el-table-column
                label="Layover Score"
            >
                <template #default="scope">
                    {{ scope.row.layover_score ?? "N/A" }}
                </template>
            </el-table-column>

            <el-table-column
                label="Time Score"
            >
                <template #default="scope">
                    {{ scope.row.time_score ?? "N/A" }}
                </template>
            </el-table-column>

            <el-table-column
                label="Final Score"
            >
                <template #default="scope">
                    {{ scope.row.final_score ?? "N/A" }}
                </template>
            </el-table-column>

        </el-table>


        <!-- ========================= -->
        <!-- Segments -->
        <!-- ========================= -->

        <h3>Flight Segments</h3>

        <el-table
            :data="selectedFlight.segments"
            border
            style="width: 100%"
        >

            <el-table-column
                label="From"
            >
                <template #default="scope">
                    {{ scope.row.departure_airport.iata_code }}
                    <br>
                    {{ scope.row.departure_airport.name }}
                </template>
            </el-table-column>


            <el-table-column
                label="Departure"
            >
                <template #default="scope">
                    {{ scope.row.departure_time }}
                </template>
            </el-table-column>


            <el-table-column
                label="To"
            >
                <template #default="scope">
                    {{ scope.row.arrival_airport.iata_code }}
                    <br>
                    {{ scope.row.arrival_airport.name }}
                </template>
            </el-table-column>


            <el-table-column
                label="Arrival"
            >
                <template #default="scope">
                    {{ scope.row.arrival_time }}
                </template>
            </el-table-column>

        </el-table>

    </div>
</el-dialog>

</template>