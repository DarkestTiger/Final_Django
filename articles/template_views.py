from django.shortcuts import render


def article_list_template_view(request):
    bear_list = [
        {
            "name": "아빠곰",
            "tags": ["아빠"],
        },
        {
            "name": "엄마곰",
            "tags": ["엄마"],
        },
        {
            "name": "애기곰",
            "tags": ["애기"],
        },
    ]

    bear_list = ["사나운곰"]
    return render(request, "articles/article_list.html")
