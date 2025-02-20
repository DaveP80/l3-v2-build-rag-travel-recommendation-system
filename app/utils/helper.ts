export function makePrompt(args: any[]) {
    let prompt = "";
    let rejCount = 0;
    args.forEach((item: string, idx: number) => {
        if (item) item = item.trim();
        if (idx === 0) {
            if (!item) {
                rejCount += 1;
                item = "man or woman"
            } 
                prompt += item + " "
        }
        if (idx === 1) {
            if (!item) {
                rejCount += 1;
                item = "21"
            } 
            prompt += `age of ${item}, `
        }
        if (idx === 2) {
            if (!item) {
                item = "high school"
            }
            prompt += `education level of ${item}, `
        }
        if (idx === 3) {
            if (!item) {
                rejCount += 1;
                item = "private location"
            }
            prompt += `located at ${item}, `
        }
        if(idx === 4) {
            if (!item) {
                item = "";
            }
            prompt += `${!item ? "doesnt travel with pets" : "with pets; "}${item}`
        }
        if (idx === 5) {
            if (!Boolean(item)) {
                prompt += ""
            } else {
                prompt += ", and the environment is a concern"
            }
        }
    })
    if (prompt.length > 5) {
        prompt += " enjoy going on?"
    } else {
        return null;
    }
    if (rejCount == 3) {
        return null;
    }
    console.log(prompt)
    return prompt;
}