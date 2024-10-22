"use client"

import { Inject,ScheduleComponent, ViewDirective, ViewsDirective,
        Day, Week, Month, ResourcesDirective, ResourceDirective, 
        TimelineViews, TimelineMonth, Agenda, Resize, DragAndDrop} from '@syncfusion/ej2-react-schedule';
import '../Calendar.css';


const HRCalendar = () => {

    function Schedule(id, subject, startTime, endTime, isAllDay, teamId, scheduleId) {
        this.Id = id;
        this.Subject = subject;
        this.StartTime = new Date(startTime); // Ensure StartTime is a Date object
        this.EndTime = new Date(endTime);     // Ensure EndTime is a Date object
        this.IsAllDay = isAllDay;
        this.TeamId = teamId;
        this.ScheduleId = scheduleId;
    }

    function createScheduleDataFromJSON(jsonData) {
        return jsonData.map(event => 
            new Schedule(
                event.Id,
                event.Subject,
                event.StartTime,
                event.EndTime,
                event.IsAllDay,
                event.TeamId,
                event.ScheduleId
            )
        );
    }




    const workDays = [0, 1, 2, 3, 4, 5];
    const data = [
        {
            Id: 1,
            Subject: "AL - pers1",
            StartTime: new Date(2024,9,23,13,0), //take note, the 8 is somehow september
            EndTime: new Date(2024,9,23,18,0),
            IsAllDay: false,
            TeamId: 1, //corresponds to team
            ScheduleId: 1 // corresponds to person
        },
        {
            Id: 2,
            Subject: "ML",
            StartTime: new Date(2024,9,21,8,0),
            EndTime: new Date(2024,9,21,12,0),
            IsAllDay: false,
            TeamId: 1, //corresponds to team
            ScheduleId: 2 // corresponds to person
        },
        {
            Id: 3,
            Subject: "full-day",
            StartTime: new Date(2024,9,24,8,0),
            EndTime: new Date(2024,9,24,12,0),
            IsAllDay: false,
            TeamId: 2, //corresponds to team
            ScheduleId: 3 // corresponds to person
        },
        {
            Id: 4,
            Subject: "AL - pers2",
            StartTime: new Date(2024,9,25,13,0), //take note, the 8 is somehow september
            EndTime: new Date(2024,9,25,18,0),
            IsAllDay: false,
            TeamId: 3, //corresponds to team
            ScheduleId: 5 // corresponds to person
        },
 
    ]
    console.log(data);

    const teamData = [
        { text: 'TEAM 1', id: 1, color: '#cb6bb2' },
        { text: 'TEAM 2', id: 2, color: '#56ca85' },
        { text: 'TEAM 3', id: 3, color: '#df5286' }
    ];
    const staffData = [
        { text: 'Nancy', id: 1, groupId: 1, color: '#df5286' },
        { text: 'Steven', id: 2, groupId: 1, color: '#7fa900' },
        { text: 'Robert', id: 3, groupId: 2, color: '#ea7a57' },
        { text: 'Smith', id: 4, groupId: 2, color: '#5978ee' },
        { text: 'Michael', id: 5, groupId: 3, color: '#df5286' },
        { text: 'Root', id: 6, groupId: 3, color: '#00bdae' }
    ];

    return (
        <div className="scheduler" height={"100vh"} >
            <ScheduleComponent 
            width='100%' 
            height='650px'
            eventSettings={{ dataSource: data }}
            group={{ resources: ['Projects', 'Categories'] }}
            workDays={workDays}
            selectedDate={new Date()} 
            currentView='TimelineWeek'
            startHour = {'08:00'}>
                 <ResourcesDirective>
                    <ResourceDirective field='TeamId' title='Choose Project' name='Projects' allowMultiple={false} dataSource={teamData} textField='text' idField='id' colorField='color'/>
                    <ResourceDirective field='ScheduleId' title='Category' name='Categories' allowMultiple={true} dataSource={staffData} textField='text' idField='id' groupIDField='groupId' colorField='color'/>
                </ResourcesDirective>
                <ViewsDirective>
                    <ViewDirective option ="Day" showWeekend={false} readonly={true} />
                    <ViewDirective option='TimelineWorkWeek' showWeekend={false} readonly={true} />
                    {/* <ViewDirective option='Week' showWeekend={false} readonly={true} /> */}
                    <ViewDirective option='Month' showWeekend={false} readonly={true} />
                </ViewsDirective>
                <Inject services={[TimelineViews, TimelineMonth, Agenda, Resize, DragAndDrop,Day, Week, Month]}/>
             
            </ScheduleComponent>
        <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </div>
    );
 }

export default  HRCalendar;