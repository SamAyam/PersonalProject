using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SelectedNotesScript : MonoBehaviour {
    public Button backB;
    public Button deleteB;
    public GameObject saveEditButton;
    //public TaskButtonsScript bottomBScript;
    public List<NoteObject> selectedList;
    public bool selecting;
    public NewNoteScript nnScript;
    public GameObject optionsPanel;
    public GameObject allUI;
    public GameObject viewButtons;
    public InputField nameInput;
    public Dropdown notebookInput;
    public InputField noteInput;

    public void SelectNote(NoteObject note)
    {
        if (selecting)
        {
            selectedList.Add(note);
        }
        else  // This is to view a single note on click:
        {
            ViewNote(note);
        }
    }

    public void ViewNote(NoteObject note)
    {
        nnScript.noteToEdit = note.myNote;
        nnScript.gameObject.SetActive(true);
        saveEditButton.SetActive(true);
        nnScript.PrepScreen();
        viewButtons.SetActive(true);
        nameInput.interactable = false;
        notebookInput.interactable = false;
        noteInput.interactable = false;
    }

    public void DeselectNote(NoteObject note)
    {
        selectedList.Remove(note);
    }

    public void SetSelecting(bool sel)
    {
        selecting = sel;
    }
    
    private void Awake()
    {

        backB.onClick.AddListener(delegate { BackB(); });
        deleteB.onClick.AddListener(delegate { DeleteB(); });
    }

    private void OnDisable()
    {
        optionsPanel.SetActive(false);
    }

    private void BackB()
    {
        List<GameObject> deleteList = new List<GameObject>();
        foreach (NoteObject note in selectedList)
        {
            deleteList.Add(note.transform.Find("TaskClickedPanel").gameObject);
        }
        foreach (GameObject note in deleteList)
        {
            note.SetActive(false);
        }
        selectedList = new List<NoteObject>();
        selecting = false;
        this.gameObject.SetActive(false);
    }

    private void DeleteB()
    {
        //TODO: punishments? deduct points?
        //this.transform.parent.gameObject.SetActive(false);
        foreach (NoteObject note in selectedList)
        {
            AppControl.control.noteTrashList.Add(note.myNote);
            AppControl.control.notesList.Remove(note.myNote);
        }

        selectedList = new List<NoteObject>();
        selecting = false;
        this.gameObject.SetActive(false);

        allUI.SetActive(false);
        allUI.SetActive(true);


    }

}
