"use client"

import { Inject,ScheduleComponent, ViewDirective, ViewsDirective, Day, Week, Month } from '@syncfusion/ej2-react-schedule';
import '../Calendar.css';


const Calendar = () => {
    const data = [
        {
            Id: 1,
            Subject: "AL",
            StartTime: new Date(2024,8,21,13,0), //take note, the 8 is somehow september
            EndTime: new Date(2024,8,21,18,0),
            IsAllDay: false,
        },
        {
            Id: 2,
            Subject: "ML",
            StartTime: new Date(2024,8,22,8,0),
            EndTime: new Date(2024,8,22,12,0),
            IsAllDay: false,
        },
 
    ]
    console.log(data);

    return (
        <div className="scheduler" height={"70vh"} >
            <ScheduleComponent height={"70%"} eventSettings={{dataSource:data,}}>
                <ViewsDirective>
                    <ViewDirective option ="Day"/>
                    <ViewDirective option='Week' />
                    <ViewDirective option='Month' />
                </ViewsDirective>

                <Inject services = {[Day, Week, Month]}/>
            </ScheduleComponent>
        <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </div>
    );
 }

export default Calendar;