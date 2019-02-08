using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;
using UnityEngine.SceneManagement;


public class AppControl : MonoBehaviour
{

    //This makes 'control' accessible anywhere:
    public static AppControl control;

    //Can access in any script with AppControl.control.THE_LIST_YOU_WANT:
    public List<string> taskFoldersList;
    public List<TaskObject> tasksList;
    public List<TaskObject> donesList;
    public List<TaskObject> trashList;
    public List<HabitObject> habitsList;
    public List<HabitObject> habitsTrashList;
    public List<HabitObject> snapsList;
    public List<GameObject> goalsList;
    public List<TaskObject> projsList;
    public List<GameObject> rewardsList;
    public List<NoteObject> notesList;
    public List<string> notebooksList;
    public List<NoteObject> noteTrashList;


    public GameObject tasksScreen;
    public GameObject habitsScreen;
    public GameObject dailyScreen;
    public GameObject weeklyScreen;
    public GameObject monthlyScreen;
    public GameObject yearlyScreen;



    public TaskObject blankTask;
    public HabitObject blankHabit;
    public NoteObject blankNote;

    public DateTime lastResetDate;

    //public List<GameObject> selectedList;

    public int userPoints = 0;
    public int activePanel = 1;


    public bool autosave;      // This bool turns on autosave feature.


    //private List<string> m_taskFoldersList;
    //private List<TaskObject> m_tasksList;
    //private List<TaskObject> m_donesList;
    //private List<TaskObject> m_trashList;
    //private List<HabitObject> m_habitsList;
    //private List<HabitObject> m_snapsList;
    //private List<GameObject> m_goalsList;
    //private List<TaskObject> m_projsList;
    //private List<GameObject> m_rewardsList;
    //private List<NoteObject> m_notesList;
    //private List<string> m_notebooksList;
    //private List<NoteObject> m_noteTrashList;

    //Make sure only one AppControl instance exists:
    void Awake()
    {
        if (control == null)
        {
            DontDestroyOnLoad(gameObject);
            control = this;

            TouchScreenKeyboard.hideInput = true;

            lastResetDate = DateTime.Today;  // This gets replaced in onEnable Load

            taskFoldersList = new List<string>();
            tasksList = new List<TaskObject>();
            donesList = new List<TaskObject>();
            trashList = new List<TaskObject>();
            habitsList = new List<HabitObject>();
            snapsList = new List<HabitObject>();
            goalsList = new List<GameObject>();
            projsList = new List<TaskObject>();
            rewardsList = new List<GameObject>();
            notesList = new List<NoteObject>();
            notebooksList = new List<string>();
            noteTrashList = new List<NoteObject>();

            //m_taskFoldersList = taskFoldersList;
            //m_tasksList = tasksList;
            //m_donesList = donesList;
            //m_trashList = trashList;
            //m_habitsList = habitsList;
            //m_snapsList = snapsList;
            //m_goalsList = goalsList;
            //m_projsList = projsList;
            //m_rewardsList = rewardsList;
            //m_notesList = notesList;
            //m_notebooksList = notebooksList;
            //m_noteTrashList = noteTrashList;

            print("Make default folders here"); //????  taskFoldersList.Add("Inbox");
        }
        else if (control != this)
        {
            Destroy(gameObject);
        }
    }

    //Autoload and autosave:
    void OnEnable()
    {
        if (autosave)
        {
            control.Load();
            control.ResetObjects();
        }
    }
    void OnDisable()
    {
        //if (autosave)
        //{
        //    control.Save();
        //    print("Auto save");
        //}
    }

    private void Update()
    {
        if (activePanel == 1)  //tasks
        {
            tasksScreen.SetActive(true);
            habitsScreen.SetActive(false);
            dailyScreen.SetActive(false);
            weeklyScreen.SetActive(false);
            monthlyScreen.SetActive(false);
            yearlyScreen.SetActive(false);
        }
        else if (activePanel == 2)  //habits
        {
            tasksScreen.SetActive(false);
            habitsScreen.SetActive(true);
            dailyScreen.SetActive(false);
            weeklyScreen.SetActive(false);
            monthlyScreen.SetActive(false);
            yearlyScreen.SetActive(false);
        }
        else if (activePanel == 3)  //dailies
        {
            tasksScreen.SetActive(false);
            habitsScreen.SetActive(false);
            dailyScreen.SetActive(true);
            weeklyScreen.SetActive(false);
            monthlyScreen.SetActive(false);
            yearlyScreen.SetActive(false);
        }
        else if (activePanel == 4) //weeklies
        {
            tasksScreen.SetActive(false);
            habitsScreen.SetActive(false);
            dailyScreen.SetActive(false);
            weeklyScreen.SetActive(true);
            monthlyScreen.SetActive(false);
            yearlyScreen.SetActive(false);
        }
        else if (activePanel == 5) //monthlies
        {
            tasksScreen.SetActive(false);
            habitsScreen.SetActive(false);
            dailyScreen.SetActive(false);
            weeklyScreen.SetActive(false);
            monthlyScreen.SetActive(true);
            yearlyScreen.SetActive(false);
        }
        else if (activePanel == 6) //yearlies
        {
            tasksScreen.SetActive(false);
            habitsScreen.SetActive(false);
            dailyScreen.SetActive(false);
            weeklyScreen.SetActive(false);
            monthlyScreen.SetActive(false);
            yearlyScreen.SetActive(true);
        }
    }

    public void SetActiveScreen(int panel)
    {
        activePanel = panel;
    }

    public void LoadDailyScreen(int screen)
    {
        activePanel = 3;
        dailyScreen.GetComponent<ActiveScreenScript>().activeScreen = screen;
    }

    public void LoadWeeklyScreen(int screen)
    {
        activePanel = 4;
        weeklyScreen.GetComponent<ActiveScreenScript>().activeScreen = screen;
    }


    public void LoadMonthlyScreen(int screen)
    {
        activePanel = 5;
        monthlyScreen.GetComponent<ActiveScreenScript>().activeScreen = screen;
    }

    public void LoadYearlyScreen(int screen)
    {
        activePanel = 6;
        yearlyScreen.GetComponent<ActiveScreenScript>().activeScreen = screen;
    }

    

    public void EmptyTrash()
    {
        List<TaskObject> deleteList = new List<TaskObject>();
        foreach (TaskObject task in trashList)
        {
            deleteList.Add(task);
        }
        foreach (TaskObject task in deleteList)
        {
            Destroy(task.gameObject);
        }
        trashList = new List<TaskObject>();
    }

    public void EmptyDones()
    {
        List<TaskObject> deleteList = new List<TaskObject>();
        foreach (TaskObject task in donesList)
        {
            deleteList.Add(task);
        }
        foreach (TaskObject task in deleteList)
        {
            Destroy(task.gameObject);
        }
        donesList = new List<TaskObject>();
    }

    public void EmptyTrashHabits()
    {
        List<HabitObject> deleteList = new List<HabitObject>();
        foreach (HabitObject habit in habitsTrashList)
        {
            deleteList.Add(habit);
        }
        foreach (HabitObject task in deleteList)
        {
            Destroy(task.gameObject);
        }
        habitsTrashList = new List<HabitObject>();
    }

    public void HabitReset(HabitObject habit)
    {
        if (habit.done)
        {
            habit.done = false;
        }
        else
        {
            //if (onVacation == false){}
            // TODO: put punishments/consequences function here
            if (habit.missed)
            {
                habit.inARow += 1;
            }
            else
            {
                habit.missed = true;
                habit.inARow = 1;
                habit.yellowCircle.SetActive(false);
                habit.blueCircle.SetActive(false);
                habit.redCircle.SetActive(true);
            }
        }
    }

    public void SnapReset(HabitObject snap)
    {
        if (snap.done)
        {
            snap.done = false;
        }
        else
        {
            //if (onVacation == false){}
            // TODO: put punishments/consequences function here
            if (snap.missed)
            {
                snap.inARow += 1;
            }
            else
            {
                snap.missed = true;
                snap.inARow = 1;
                snap.yellowCircle.SetActive(false);
                snap.redCircle.SetActive(false);
                snap.blueCircle.SetActive(true);
            }
        }
    }

    public void SimulateDays()
    {
        int daysLeft = DateTime.Today.Subtract(lastResetDate).Days;
        while (daysLeft > 0)
        {
            DateTime thisDay = DateTime.Today.AddDays(1-daysLeft);
            print("ThisDay in simulation is = " + thisDay);

            foreach (HabitObject habit in habitsList)
            {
                if (thisDay.Subtract(habit.resetDate).Days >= 0)
                {
                    print("Habit  " + habit.name + "  reached or passed reset date.");
                    if (habit.repeatType == 1)
                    {
                        if (habit.daysOfWeek.Count == 0 || habit.daysOfWeek.Contains(thisDay.DayOfWeek))
                        {
                            HabitReset(habit);
                        }
                    }
                    else if (habit.repeatType == 2)
                    {

                        if (thisDay.DayOfWeek == 0)
                        {
                            HabitReset(habit);
                        }
                    }
                    else if (habit.repeatType == 3)
                    {
                        if (thisDay.Day == 1)
                        {
                            HabitReset(habit);
                        }
                    }
                    else if (habit.repeatType == 4)
                    {
                        if (thisDay.DayOfYear == 1)
                        {
                            HabitReset(habit);
                        }
                    }
                    else if (habit.repeatType == 0) // 0 = constant
                    {
                        habit.done = false;
                    }
                }
            }
            foreach (HabitObject snap in snapsList)
            {
                if (thisDay.Subtract(snap.resetDate).Days >= 0)
                {
                    if (snap.repeatType == 1)
                    {
                        if (snap.daysOfWeek.Count == 0 || snap.daysOfWeek.Contains(thisDay.DayOfWeek))
                        {
                            SnapReset(snap);
                        }
                    }
                }
                else if (snap.repeatType == 2)
                {
                    if (thisDay.DayOfWeek == 0)
                    {
                        SnapReset(snap);
                    }
                }
                else if (snap.repeatType == 3)
                {
                    if (thisDay.Day == 1)
                    {
                        SnapReset(snap);
                    }
                }
                else if (snap.repeatType == 4)
                {
                    if (thisDay.DayOfYear == 1)
                    {
                        SnapReset(snap);
                    }
                }
                else if (snap.repeatType == 0) // 0 = constant
                {
                    snap.done = false;
                }
            }
            daysLeft -= 1;
        }
    }


    public void ResetObjects()
    {
        if (System.DateTime.Today.Subtract(lastResetDate).Days >= 1)
        {
            print("reset");
            SimulateDays();
            lastResetDate = DateTime.Today;
        }
        //if (autosave)
        //{
        //    control.Save();
        //    print("Autosaved");
        //}
    }

    private List<TaskData> NewTaskSave(List<TaskObject> _List)
    {

        List<TaskData> _saveList = new List<TaskData>();
        for (int i = 0; i < _List.Count; i++)
        {
            TaskData dat = new TaskData();
            dat.taskName = _List[i].taskName;
            dat.taskFolder = _List[i].taskFolder;
            dat.dueDate = _List[i].dueDate;
            dat.optional = _List[i].optional;
            dat.repeatType = _List[i].repeatType;
            dat.priority = _List[i].priority;
            dat.userTags = _List[i].userTags;
            dat.comments = _List[i].comments;
            //dat.myParentTask = _List[i].myParentTask;
            _saveList.Add(dat);
        }
        return _saveList;
    }

    private List<HabitData> NewHabitSave(List<HabitObject> _List)
    {
        List<HabitData> _saveList = new List<HabitData>();
        for (int i = 0; i < _List.Count; i++)
        {
            HabitData dat = new HabitData();
            dat.habitName = _List[i].habitName;
            dat.repeatType = _List[i].repeatType;
            dat.doItList = _List[i].doItList;
            dat.rewardPoints = _List[i].rewardPoints;
            dat.missedPoints = _List[i].missedPoints;
            //dat.rewardToken = _List[i].rewardToken;
            //dat.missedLoss = _List[i].missedLoss;
            dat.showPoints = _List[i].showPoints;
            dat.asleep = _List[i].asleep;
            dat.done = _List[i].done;
            dat.resetDate = _List[i].resetDate;
            dat.inARow = _List[i].inARow;
            dat.missed = _List[i].missed;
            dat.daysOfWeek = _List[i].daysOfWeek;
            _saveList.Add(dat);
        }
        return _saveList;
    }

    private List<NoteData> NewNoteSave(List<NoteObject> _List)
    {

        List<NoteData> _saveList = new List<NoteData>();
        for (int i = 0; i < _List.Count; i++)
        {
            NoteData dat = new NoteData();
            dat.noteName = _List[i].noteName;
            dat.notebook = _List[i].notebook;
            dat.noteString = _List[i].noteString;
            dat.createdDate = _List[i].createdDate;
            dat.modifiedDate = _List[i].modifiedDate;
            //dat.priority = _List[i].priority;
            //dat.userTags = _List[i].userTags;
            //dat.comments = _List[i].comments;
            _saveList.Add(dat);
        }
        return _saveList;
    }

    //Can access in any script with AppControl.control.Save()
    public void Save()
    {
        UserData data = new UserData();
        data.lastResetDate = lastResetDate;

        data.taskFoldersList = taskFoldersList;

        //data.tasksList = tasksList;
        data.tasksList = NewTaskSave(tasksList);

        //data.donesList = donesList;
        data.donesList = NewTaskSave(donesList);

        //data.trashList = trashList;
        data.trashList = NewTaskSave(trashList);

        //data.habitsList = habitsList;
        data.habitsList = NewHabitSave(habitsList);

        //data.snapsList = snapsList;
        data.snapsList = NewHabitSave(snapsList);

        data.goalsList = goalsList;

        //data.ProjsList = ProjsList;
        data.projsList = NewTaskSave(projsList);

        data.rewardsList = rewardsList;

        //data.notesList = notesList;
        data.notesList = NewNoteSave(notesList);

        data.notebooksList = notebooksList;

        //data.noteTrashList = noteTrashList;
        data.noteTrashList = NewNoteSave(noteTrashList);

        data.activePanel = activePanel;
        data.dailyActivePanel = dailyScreen.GetComponent<ActiveScreenScript>().activeScreen;
        data.weeklyActivePanel = weeklyScreen.GetComponent<ActiveScreenScript>().activeScreen;
        data.monthlyActivePanel = monthlyScreen.GetComponent<ActiveScreenScript>().activeScreen;
        data.yearlyActivePanel = yearlyScreen.GetComponent<ActiveScreenScript>().activeScreen;

        BinaryFormatter bf = new BinaryFormatter();
        FileStream file = File.Create(Application.persistentDataPath + "/userInfo.dat");
        bf.Serialize(file, data);
        file.Close();
        print("Save Complete");
    }

    private List<TaskObject> NewTaskLoad(List<TaskData> dataList)
    {
        List<TaskObject> _loadList = new List<TaskObject>();
        for (int i = 0; i < dataList.Count; i++)
        {
            TaskObject newTaskInstance = Instantiate(blankTask) as TaskObject;
            newTaskInstance.taskName = dataList[i].taskName;
            newTaskInstance.taskFolder = dataList[i].taskFolder;
            newTaskInstance.dueDate = dataList[i].dueDate;
            newTaskInstance.optional = dataList[i].optional;
            newTaskInstance.repeatType = dataList[i].repeatType;
            newTaskInstance.priority = dataList[i].priority;
            newTaskInstance.userTags = dataList[i].userTags;
            newTaskInstance.comments = dataList[i].comments;
            _loadList.Add(newTaskInstance);
        }
        return _loadList;
    }

    private List<HabitObject> NewHabitLoad(List<HabitData> dataList)
    {
        List<HabitObject> _loadList = new List<HabitObject>();
        for (int i = 0; i < dataList.Count; i++)
        {
            HabitObject newHabitInstance = Instantiate(blankHabit) as HabitObject;
            newHabitInstance.habitName = dataList[i].habitName;
            newHabitInstance.repeatType = dataList[i].repeatType;
            newHabitInstance.doItList = dataList[i].doItList;
            newHabitInstance.rewardPoints = dataList[i].rewardPoints;
            newHabitInstance.missedPoints = dataList[i].missedPoints;
            //newHabitInstance.rewardToken = dataList[i].rewardToken;
            //newHabitInstance.missedLoss = dataList[i].missedLoss;
            newHabitInstance.showPoints = dataList[i].showPoints;
            newHabitInstance.asleep = dataList[i].asleep;
            newHabitInstance.done = dataList[i].done;
            newHabitInstance.resetDate = dataList[i].resetDate;
            newHabitInstance.inARow = dataList[i].inARow;
            newHabitInstance.missed = dataList[i].missed;
            newHabitInstance.daysOfWeek = dataList[i].daysOfWeek;
            _loadList.Add(newHabitInstance);
        }
        return _loadList;
    }

    private List<NoteObject> NewNoteLoad(List<NoteData> dataList)
    {
        List<NoteObject> _loadList = new List<NoteObject>();
        for (int i = 0; i < dataList.Count; i++)
        {
            NoteObject newNoteInstance = Instantiate(blankNote) as NoteObject;
            newNoteInstance.noteName = dataList[i].noteName;
            newNoteInstance.notebook = dataList[i].notebook;
            newNoteInstance.noteString = dataList[i].noteString;
            newNoteInstance.createdDate = dataList[i].createdDate;
            newNoteInstance.modifiedDate = dataList[i].modifiedDate;
            //newNoteInstance.priority = dataList[i].priority;
            //newNoteInstance.userTags = dataList[i].userTags;
            //newNoteInstance.comments = dataList[i].comments;
            _loadList.Add(newNoteInstance);
        }
        return _loadList;
    }

    //Can access in any script with AppControl.control.Load()
    public void Load()                                                // TODO: WHEN FILLING IN CHILDRENTASKS IN TASK SET MYPARENT FOR EACH CHILD (not saved)
    {
        if (File.Exists(Application.persistentDataPath + "/userInfo.dat"))
        {
            BinaryFormatter bf = new BinaryFormatter();
            FileStream file = File.Open(Application.persistentDataPath + "/userInfo.dat", FileMode.Open);
            UserData data = (UserData)bf.Deserialize(file);
            file.Close();

            lastResetDate = data.lastResetDate;

            taskFoldersList = data.taskFoldersList;
            tasksList = new List<TaskObject>();
            donesList = new List<TaskObject>();
            trashList = new List<TaskObject>();
            habitsList = new List<HabitObject>();
            snapsList = new List<HabitObject>();
            goalsList = new List<GameObject>();
            projsList = new List<TaskObject>();
            rewardsList = new List<GameObject>();
            notesList = new List<NoteObject>();
            notebooksList = new List<string>();
            noteTrashList = new List<NoteObject>();

            // tasksList = data.tasksList:
            tasksList = NewTaskLoad(data.tasksList);

            //donesList = data.donesList;
            donesList = NewTaskLoad(data.donesList);

            //trashList = data.trashList;
            trashList = NewTaskLoad(data.trashList);

            // habitsList = data.habitsList:
            habitsList = NewHabitLoad(data.habitsList);

            //snapsList = data.snapsList;
            snapsList = NewHabitLoad(data.snapsList);

            goalsList = data.goalsList;

            //ProjsList = data.ProjsList;
            projsList = NewTaskLoad(data.projsList);

            rewardsList = data.rewardsList;

            //notesList = data.notesList;
            notesList = NewNoteLoad(data.notesList);

            notebooksList = data.notebooksList;

            //noteTrashList = data.noteTrashList;
            noteTrashList = NewNoteLoad(data.noteTrashList);

            
            dailyScreen.GetComponent<ActiveScreenScript>().activeScreen = data.dailyActivePanel;
            weeklyScreen.GetComponent<ActiveScreenScript>().activeScreen = data.weeklyActivePanel;
            monthlyScreen.GetComponent<ActiveScreenScript>().activeScreen = data.monthlyActivePanel;
            yearlyScreen.GetComponent<ActiveScreenScript>().activeScreen = data.yearlyActivePanel;
            activePanel = data.activePanel;

            ResetObjects();

            print("Load Complete");
        }
        else
        {
            print("Load File Not Found");
        }
    }
}



//This is the object that is saved:
[Serializable]
class UserData
{
    public int userPoints = 0;
    public int activePanel = 1;
    public int dailyActivePanel;
    public int weeklyActivePanel;
    public int monthlyActivePanel;
    public int yearlyActivePanel;
    public DateTime lastResetDate;
    public List<string> taskFoldersList = new List<string>();
    public List<TaskData> tasksList = new List<TaskData>();
    public List<TaskData> donesList = new List<TaskData>();
    public List<TaskData> trashList = new List<TaskData>();
    public List<HabitData> habitsList = new List<HabitData>();
    public List<HabitData> snapsList = new List<HabitData>();
    public List<GameObject> goalsList = new List<GameObject>();
    public List<TaskData> projsList = new List<TaskData>();
    public List<GameObject> rewardsList = new List<GameObject>();
    public List<NoteData> notesList = new List<NoteData>();
    public List<string> notebooksList = new List<string>();
    public List<NoteData> noteTrashList = new List<NoteData>();
}

[Serializable]
class TaskData
{
    public string taskName;
    public string taskFolder;
    public DateTime dueDate;
    public bool optional;
    public int repeatType;
    public int priority;
    public List<string> userTags;
    public List<CommentObject> comments;
}

[Serializable]
class HabitData
{
    public string habitName;
    public int repeatType;
    public List<DoItObject> doItList;
    public int rewardPoints;
    public int missedPoints;
    //public object rewardToken;
    //public object missedLoss;
    public bool showPoints;
    public bool asleep;
    public bool done;
    public DateTime resetDate;
    public int inARow;
    public bool missed;
    public List<DayOfWeek> daysOfWeek;
}

[Serializable]
class NoteData
{
    public string noteName;
    public string notebook;
    public string noteString;
    public DateTime createdDate;
    public DateTime modifiedDate;
    //newNoteInstance.priority = dataList[i].priority;
    //newNoteInstance.userTags = dataList[i].userTags;
    //newNoteInstance.comments = dataList[i].comments;
}