using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;

public class AddCommentToTask : MonoBehaviour
{
    public CommentObject blankComment;
    public InputField commentInput;
    public GameObject allUI;
    public TaskObject taskToEdit;
    public List<CommentObject> selectedComments = new List<CommentObject>();
    public GameObject deleteButton;

    private void Update()
    {
        if (selectedComments.Count >= 1)
        {
            deleteButton.SetActive(true);
        }
        else
        {
            deleteButton.SetActive(false);
        }
    }

    public void PrepScreen()
    {
        commentInput.text = "";   // For some reason this make the InputField give an error, then it runs LateUpdate() to fix it.
        commentInput.Select();    // This seems to work fine, ignore the error message for now.
    }

    public void Delete()
    {
        List<CommentObject> deleteList = new List<CommentObject>();
        foreach(CommentObject comment in selectedComments)
        {
            taskToEdit.comments.Remove(comment.myComment);
            deleteList.Add(comment);
        }
        foreach(CommentObject comment in deleteList)
        {
            Destroy(comment.myComment.gameObject);
            Destroy(comment.gameObject);
        }

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    public void AddComment()
    {
        if (commentInput.text.Trim() != "")
        {
            CommentObject newCommentInstance = Instantiate(blankComment) as CommentObject;

            newCommentInstance.commentString = commentInput.text;

            newCommentInstance.createdDate = DateTime.Now;

            newCommentInstance.myTask = taskToEdit;
            
            taskToEdit.comments.Add(newCommentInstance);

            allUI.SetActive(false);
            allUI.SetActive(true);


            PrepScreen();

            if (AppControl.control.autosave)
            {
                AppControl.control.Save();
            }
        }
        else
        {
            print("Cannot save a blank comment.");
        }
    }
}