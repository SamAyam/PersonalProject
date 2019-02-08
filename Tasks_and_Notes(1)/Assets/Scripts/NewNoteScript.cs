using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;
using TMPro;

public class NewNoteScript : MonoBehaviour
{
    public NoteObject blankNote;
    public InputField noteName;
    public Dropdown notebookBox;
    public InputField noteContent;
    public Button noteContentButton;
    public GameObject allUI;
    public NoteObject noteToEdit;   // This variable is set by the "edit" button in "MakeEditButtons"
    public InputField notebookName;
    public Text noteContentText;
    public string noteString;
    public bool editing;


    public GameObject viewButtons;
    public InputField nameInput;
    public Dropdown notebookInput;
    public InputField noteInput;


    public GameObject newNotebookWindow;

    //ADDITIONAL OPTIONS:

    //public int repeatType;
    //public InputField dueDate;
    //public List<String> userTags;
    //public InputField tagsInput;
    //public Dropdown repeatTypeInput;
    //public InputField rewardToken;
    //public InputField missedLoss;

    public void ClearEdit()
    {
        noteToEdit = null;
    }

    //private void OnEnable()
    //{
    //    PrepScreen();
    //}

    public void PrepScreen()
    {
        notebookBox.ClearOptions();

        if (AppControl.control.notebooksList.Contains("Inbox") == false)
        {
            AppControl.control.notebooksList.Add("Inbox");
            AppControl.control.notebooksList.Add("test");
            print("TODO: remove 'test' notebook");  //and move Inbox to appControl? (or copy, redundant?)
        }
        notebookBox.AddOptions(AppControl.control.notebooksList);
        List<string> tempList = new List<string> { "Add New Folder" };
        notebookBox.AddOptions(tempList);

        RectTransform trans = noteContent.GetComponent<RectTransform>();
        noteContent.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, 600);
        noteContent.GetComponent<LayoutElement>().minHeight = 600;
        trans.sizeDelta = new Vector2(trans.sizeDelta.x, 600);
        trans.GetComponent<LayoutElement>().minHeight = 600;
        noteContentText.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, 600);
        noteContentText.GetComponent<LayoutElement>().minHeight = 600;
        noteContentButton.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, 600);
        noteContentButton.GetComponent<LayoutElement>().minHeight = 600;
        trans.parent.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.parent.GetComponent<RectTransform>().sizeDelta.x, 600);
        trans.parent.GetComponent<LayoutElement>().minHeight = 600;

        try
        {
            noteName.text = noteToEdit.noteName;
            
            notebookBox.value = AppControl.control.notebooksList.IndexOf(noteToEdit.notebook);

            noteContent.text = noteToEdit.noteString;


            noteContent.interactable = false;

            ResizeInput();
        }
        catch (Exception) //e)
        {
            //Debug.LogException(e, this);

            noteName.text = "";
            notebookBox.value = 0;
            noteContent.text = "";

            noteContent.ActivateInputField();
        }
    }

    public void OpenNewNotebookWindowCheck()
    {
        print(notebookBox.value);
        print(notebookBox.options.Count);
        if (notebookBox.value == notebookBox.options.Count - 1)
        {
            newNotebookWindow.SetActive(true);
        }
    }

    public void NewNotebook()
    {
        AppControl.control.notebooksList.Add(CultureInfo.CurrentCulture.TextInfo.ToTitleCase(notebookName.text.ToLower()));

        notebookBox.ClearOptions();

        notebookBox.AddOptions(AppControl.control.notebooksList);

        List<string> tempList = new List<string> { "Add New Folder" };

        notebookBox.AddOptions(tempList);

        notebookBox.value = AppControl.control.notebooksList.IndexOf(CultureInfo.CurrentCulture.TextInfo.ToTitleCase(notebookName.text.ToLower()));

    }

    public void Create()
    {
        NoteObject newNoteInstance = Instantiate(blankNote) as NoteObject;

        if (noteName.text.Trim() == "")
        {
            newNoteInstance.noteName = "Untitled";
        }
        else
        {
            newNoteInstance.noteName = noteName.text.Trim();
        }
        newNoteInstance.notebook = notebookBox.options[notebookBox.value].text;

        newNoteInstance.noteString = noteContent.text;

        newNoteInstance.createdDate = DateTime.Now;
        newNoteInstance.modifiedDate = DateTime.Now;

        AppControl.control.notesList.Add(newNoteInstance);

        noteContent.interactable = false;

        allUI.SetActive(false);
        allUI.SetActive(true);

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }


    public void SaveEdit()
    {
        AppControl.control.notesList.Remove(noteToEdit);
        if (noteName.text.Trim() != "")
        {
            this.noteToEdit.noteName = noteName.text.Trim();
        }

        this.noteToEdit.notebook = notebookBox.options[notebookBox.value].text;

        noteToEdit.noteString = noteContent.text;

        noteToEdit.modifiedDate = DateTime.Now;

        AppControl.control.notesList.Add(noteToEdit);

        noteToEdit = null;

        noteContent.interactable = false;
        //noteContent.transform.parent.GetComponent<Button>().interactable = false;

        allUI.SetActive(false);
        allUI.SetActive(true);

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    public void ResizeInput()
    {
        TextGenerator textGen = new TextGenerator();
        TextGenerationSettings generationSettings = noteContentText.GetGenerationSettings(noteContentText.rectTransform.rect.size);
        float height = textGen.GetPreferredHeight(noteContentText.text, generationSettings);
        //float height = noteContent.fontAsset.fontInfo.AtlasHeight;

        RectTransform trans = noteContent.GetComponent<RectTransform>();
        
        if (height >= trans.sizeDelta.y -100)
        {
            noteContent.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, height + 400);
            noteContent.GetComponent<LayoutElement>().minHeight = height + 400;
            trans.sizeDelta = new Vector2(trans.sizeDelta.x, height + 400);
            trans.GetComponent<LayoutElement>().minHeight = height + 400;
            noteContentText.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, height + 400);
            noteContentText.GetComponent<LayoutElement>().minHeight = height + 400;
            noteContentButton.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, height + 400);
            noteContentButton.GetComponent<LayoutElement>().minHeight = height + 400;
            trans.parent.GetComponent<RectTransform>().sizeDelta = new Vector2(trans.sizeDelta.x, height + 400);
            trans.parent.GetComponent<LayoutElement>().minHeight = height + 400;
        }
    }

    public void SetString()
    {
        noteString = noteContent.text;
    }

    public void TurnOffViewOnly()
    {
        viewButtons.SetActive(false);
        nameInput.interactable = true;
        notebookInput.interactable = true;
        noteInput.interactable = true;
    }
}
