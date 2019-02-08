using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetNotes : MonoBehaviour
{
    public NoteObject blankNote;

    public void DrawTasks()
    {
        if (AppControl.control != null)
        {
            Clear();
            for (int i = 0; i < AppControl.control.notesList.Count; i++)
            {
                MakeNote(i);
            }

        }
    }

    public void MakeNote(int i)
    {
        NoteObject newNoteInstance = Instantiate(blankNote) as NoteObject;
        newNoteInstance.myNote = AppControl.control.notesList[i];
        newNoteInstance.notebook = AppControl.control.notesList[i].notebook;
        newNoteInstance.noteName = AppControl.control.notesList[i].noteName;
        newNoteInstance.noteString = AppControl.control.notesList[i].noteString;
        newNoteInstance.createdDate = AppControl.control.notesList[i].createdDate;
        newNoteInstance.modifiedDate = AppControl.control.notesList[i].modifiedDate;
        newNoteInstance.transform.SetParent(this.transform);
        newNoteInstance.GetComponent<RectTransform>().localScale = Vector3.one;
        newNoteInstance.Resize();
    }

    public void Clear()
    {
        foreach (Transform child in transform)
        {
            GameObject.Destroy(child.gameObject);
        }
    }

    private void OnEnable()
    {
        DrawTasks();
    }

    private void OnDisable()
    {
        Clear();
    }
}
