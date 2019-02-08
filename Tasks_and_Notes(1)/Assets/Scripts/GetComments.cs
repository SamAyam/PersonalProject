using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetComments : MonoBehaviour
{
    public CommentObject blankComment;
    public TaskObject task;

    public void DrawTasks()
    {
            Clear();
            if (task.comments.Count > 1)
            {
                task.comments.Sort((p2, p1) => p1.createdDate.CompareTo(p2.createdDate));
            }
            for (int i = 0; i < task.comments.Count; i++)
            {
                CommentObject newCommentInstance = Instantiate(blankComment) as CommentObject;
                newCommentInstance.myComment = task.comments[i];
                newCommentInstance.commentString = task.comments[i].commentString;
                newCommentInstance.createdDate = task.comments[i].createdDate;
                newCommentInstance.myTask = task.comments[i].myTask;
                newCommentInstance.transform.SetParent(this.transform);
                newCommentInstance.GetComponent<RectTransform>().localScale = Vector3.one;
                newCommentInstance.Resize();
            }
    }

    public void Clear()
    {
        foreach (Transform child in transform)
        {
            if (child.name != "CommentLabel" && child.name != "CommentInput" && child.name != "SavePanel")
            {
                GameObject.Destroy(child.gameObject);
            } 
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
