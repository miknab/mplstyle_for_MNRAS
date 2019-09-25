function mindis = MinDistance(X)
mindis = 1000;
for i = 1:length(X)-1
    for j=i+1:length(X)
        if norm(X(i,:)- X(j,:))<mindis
            mindis=norm(X(i,:)- X(j,:));
        end
    end
end
end

