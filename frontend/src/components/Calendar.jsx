"use client"

import { Inject,ScheduleComponent, ViewDirective, ViewsDirective, Day, Week, Month } from '@syncfusion/ej2-react-schedule';
import '../Calendar.css';


const Calendar = () => {
    const data = [
        {
            Id: 1,
            Subject: "AL - pers1",
            StartTime: new Date(2024,9,10,13,0), //take note, the 8 is somehow september
            EndTime: new Date(2024,9,10,18,0),
            IsAllDay: false,
        },
        {
            Id: 2,
            Subject: "ML",
            StartTime: new Date(2024,8,22,8,0),
            EndTime: new Date(2024,8,22,12,0),
            IsAllDay: false,
        },
        {
            Id: 3,
            Subject: "full-day",
            StartTime: new Date(2024,8,22,8,0),
            EndTime: new Date(2024,8,22,12,0),
            IsAllDay: false,
        },
        {
            Id: 4,
            Subject: "AL - pers2",
            StartTime: new Date(2024,9,10,13,0), //take note, the 8 is somehow september
            EndTime: new Date(2024,9,10,18,0),
            IsAllDay: false,
        },
 
    ]
    console.log(data);

    return (
        <div className="scheduler" height={"70vh"} >
            <ScheduleComponent height={"70%"} 
            eventSettings={{dataSource:data,}}>
                <ViewsDirective>
                    <ViewDirective option ="Day" showWeekend={false} readonly={true} />
                    <ViewDirective option='Week' showWeekend={false} readonly={true} startHour = {'08:00'}/>
                    <ViewDirective option='Month' showWeekend={false} readonly={true} />
                </ViewsDirective>

                <Inject services = {[Day, Week, Month]}/>
            </ScheduleComponent>
        <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </div>
    );
 }

export default Calendar;